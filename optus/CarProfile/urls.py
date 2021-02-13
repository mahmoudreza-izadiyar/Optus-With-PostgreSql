from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addCar/', views.addCar, name='addCar'),
    path('delete/<int:carId>', views.delete, name='delete'),
    path('edit/<int:carId>', views.edit, name='edit'),
    path('document/', views.document, name='document'),
    path('addByPs/', views.addByPs, name='addByPs'),
    path('showCar/', views.showCar, name='showCar'),
    path('deleteCar/<int:carId>', views.deleteCar, name='deleteCar'),
    path('editCar/<int:carId>', views.editCar, name='editCar'),


]
