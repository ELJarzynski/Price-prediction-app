from django.contrib import admin
from .models import Property, PropertyUser

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('square_feet', 'bedrooms', 'bathrooms', 'neighborhood', 'year_built', 'price')

class PropertyUserAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'is_owner')

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyUser, PropertyUserAdmin)