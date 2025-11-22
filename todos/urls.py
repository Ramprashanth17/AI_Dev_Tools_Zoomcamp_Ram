from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_todo, name='create_todo'),
    path('edit/<int:pk>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:pk>/', views.toggle_todo, name='toggle_todo'),
]