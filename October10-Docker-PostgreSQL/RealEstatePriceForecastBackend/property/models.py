from django.db import models
from user.models import User

class Property(models.Model):
    NEIGHBOURHOOD_CHOICES = [
        ('Rural', 'Rural'),
        ('Suburb', 'Suburb'),
        ('Urban', 'Urban'),
    ]

    square_feet = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    neighborhood = models.CharField(max_length=100, choices=NEIGHBOURHOOD_CHOICES)
    year_built = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bedrooms} bed, {self.bathrooms} bath in {self.get_neighborhood_display()}"

class PropertyUser(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)