from django.urls import path        # These are the standard imports
from . import views

urlpatterns = [    
    path('admin', views.admin),
    path('', views.dashboard, name='dashboard'),
    path('users/new', views.new_user, name='new_user'),
    path('users/profile', views.edit_profile, name='edit_profile'),
    path('users/show/<int:user_id>', views.show_user, name='user_info'),
    path('users/edit/<int:user_id>', views.edit_user, name='edit_user'),
    path('users/remove/<int:remove_id>', views.remove_user, name='remove_user'),
    path('update_password', views.update_password, name='update_password'),
    path('update_user', views.update_user, name='update_user'),
    path('users/show/<int:profile_id>/post_message', views.post_message, name='post_message'),
    path('users/show/<int:profile_id>/post_comment', views.post_comment, name='post_comment'),
]