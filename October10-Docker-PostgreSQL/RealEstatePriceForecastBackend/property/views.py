from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from .models import Property, PropertyUser
from .serializers import PropertySerializer, PropertyUserSerializer
import joblib
import numpy as np

# Load the model once during server startup
model = joblib.load('property/linear_regression_model_October_8.pkl')

class PredictPriceView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data  # Get data from the request
            features = np.array([
                data.get('square_feet', 0),
                data.get('bedrooms', 0),
                data.get('bathrooms', 0),
                data.get('year_built', 0),
                data.get('neighborhood_rural', 0),
                data.get('neighborhood_suburb', 0),
                data.get('neighborhood_urban', 0)
            ]).reshape(1, -1)

            predicted_price = model.predict(features)[0]
            return Response({'predicted_price': predicted_price}, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({'error': str(e)})

class CreatePropertyView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        property_instance = serializer.save()
        user = self.request.user
        property_user = PropertyUser.objects.create(
            property=property_instance,
            user=user,
            is_owner=True
        )

        data = {
            'property': PropertySerializer(property_instance).data,
            'property_user': PropertyUserSerializer(property_user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

class RetrievePropertyView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return Property.objects.filter(propertyuser__user_id=user_id)

class RetrieveSinglePropertyView(generics.RetrieveAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user_id = self.request.user.id
        property_id = self.kwargs['property_id']

        try:
            return Property.objects.get(id=property_id, propertyuser__user_id=user_id)
        except Property.DoesNotExist:
            raise NotFound("Property not found")

class CreatePropertyUserView(generics.CreateAPIView):
    queryset = PropertyUser.objects.all()
    serializer_class = PropertyUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.kwargs.get('property_id')
        user = self.request.user
        property_instance = Property.objects.get(pk=property_id)

        serializer.is_valid(raise_exception=True)
        user_instance = serializer.validated_data['user']

        property_user = PropertyUser.objects.filter(property=property_instance, user=user).first()
        if not property_user or not property_user.is_owner:
            raise PermissionDenied({'message': 'You are not the owner of this property.'})

        if PropertyUser.objects.filter(property=property_instance, user=user_instance).exists():
            raise ValidationError({'message': 'User is already assigned to this property.'})

        serializer.save(property=property_instance, user=user_instance)

class ListPropertyUsersView(generics.ListAPIView):
    serializer_class = PropertyUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        return PropertyUser.objects.filter(property=property_id)

class DeletePropertyUserView(generics.DestroyAPIView):
    queryset = PropertyUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        property_id = self.kwargs.get('property_id')
        user_id = self.kwargs.get('user_id')

        property_user = PropertyUser.objects.filter(property=property_id, user=request.user, is_owner=True).first()
        if not property_user:
            raise PermissionDenied("You are not the owner of this property.")

        try:
            property_user_to_delete = PropertyUser.objects.get(property=property_id, user=user_id)
        except PropertyUser.DoesNotExist:
            return Response({'message': 'Property user not found.'}, status=status.HTTP_404_NOT_FOUND)

        property_user_to_delete.delete()
        return Response({'message': 'Property user deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class DeletePropertyView(generics.DestroyAPIView):
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        property_id = self.kwargs.get('property_id')

        property_user = PropertyUser.objects.filter(property=property_id, user=request.user, is_owner=True).first()
        if not property_user:
            raise PermissionDenied("You are not the owner of this property.")

        try:
            property_to_delete = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({'message': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        property_to_delete.delete()
        return Response({'message': 'Property deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class UpdatePropertyView(generics.UpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        property_id = self.kwargs.get('property_id')

        try:
            property_to_edit = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({'message': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        property_user = PropertyUser.objects.filter(property=property_id, user=request.user, is_owner=True).first()
        if not property_user:
            raise PermissionDenied("You are not the owner of this property.")

        serializer = self.get_serializer(property_to_edit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
