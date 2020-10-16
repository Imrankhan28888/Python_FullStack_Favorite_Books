from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('create_book', views.create),
    path('show/<int:id>', views.show_book),
    path('edit/<int:id>', views.edit_book),
    path('delete/<int:id>', views.delete_book),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
  
]