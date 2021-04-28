from django.urls import path        # These are the standard imports
from . import views

urlpatterns = [
    path('', views.books, name="books_home"),
    path('add', views.add, name="add_book"),
    path('new_book', views.newBook, name="new_book"),
    path('update/<int:bid>', views.update, name="update_submit"),
    path('<int:bid>', views.book_info, name="book_info"),
    path('users/<int:uid>', views.user_info, name="user_books"),    
    path('delete/<int:rid>', views.del_review, name="delete_review"),
    path('favorite/<int:book_id>', views.add_favorite, name="add_favorite"),
    path('cl/<str:page>/<int:bid>', views.clear),
]