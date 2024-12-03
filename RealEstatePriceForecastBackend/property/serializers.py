from rest_framework import serializers
from property.models import Property, PropertyUser
from user.models import User
from user.serializers import UserSerializer

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'square_feet',
            'bedrooms',
            'bathrooms',
            'neighborhood',
            'year_built',
            'price',
        )

class PropertyUserSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    is_owner = serializers.BooleanField(read_only=True)

    class Meta:
        model = PropertyUser
        fields = (
            'property',
            'user',
            'user_detail',
            'is_owner',
        )
