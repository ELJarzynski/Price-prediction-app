# property/urls.py
from django.urls import path
from property.views import (
    CreatePropertyView, CreatePropertyUserView, RetrievePropertyView,
    RetrieveSinglePropertyView, ListPropertyUsersView, DeletePropertyUserView,
    DeletePropertyView, UpdatePropertyView, PredictPriceView
)

app_name = 'property'

urlpatterns = [
    path('create_property/', CreatePropertyView.as_view(), name='property-create'),
    path('add_user/', CreatePropertyUserView.as_view(), name='property-user-create'),
    path('list_property/', RetrievePropertyView.as_view(), name='property-list'),
    path('<int:property_id>/', RetrieveSinglePropertyView.as_view(), name='retrieve-property'),
    path('<int:property_id>/add_user/', CreatePropertyUserView.as_view(), name='add-user-to-property'),
    path('<int:property_id>/users/', ListPropertyUsersView.as_view(), name='property-users-list'),
    path('<int:property_id>/delete_user/<int:user_id>/', DeletePropertyUserView.as_view(), name='property-user-delete'),
    path('<int:property_id>/delete_property/', DeletePropertyView.as_view(), name='property-delete'),
    path('<int:property_id>/edit_property/', UpdatePropertyView.as_view(), name='property-edit'),
    path('predict_price/', PredictPriceView.as_view(), name='predict-price')
]
