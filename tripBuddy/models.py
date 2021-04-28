from django.db import models
from loginApp.models import User

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField() 
    end_date = models.DateTimeField() 
    details = models.TextField()
    planned_by = models.ForeignKey(User, related_name='planned_trips', on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name='extra_trips', blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
