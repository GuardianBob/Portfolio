from django.urls import path  
from . import views

urlpatterns = [
    path('', views.dashboard, name='trip_dash'),
    path('<int:trip_id>', views.trips, name='trip_info'),
    path('new', views.new_trip, name='new_trip'),
    path('create', views.create_trip, name='create_trip'),
    path('update', views.update_trip, name='update_trip'),
    path('edit/<int:trip_id>', views.edit_trip, name='edit_trip'),
    path('join/<int:trip_id>', views.join_trip, name='join_trip'),
    path('remove/<int:trip_id>', views.remove_trip, name='remove_trip'),
    path('delete/<int:trip_id>', views.delete_trip, name='delete_trip'),
    path('cancel/<int:trip_id>', views.cancel_trip, name='cancel_trip'),
    ]