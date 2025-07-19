from django.urls import path
from . import views

urlpatterns = [
    path('', views.task, name='task'),
    path('task-form/', views.taskForm, name='task-form'),
    path('update-task/<str:pk>/', views.updateTask, name='update-task'),
    path('complete-task/<str:pk>/', views.completeTask, name='complete-task'),
    path('incomplete-task/<str:pk>/', views.incompleteTask, name='incomplete-task'),
    path('delete-task/<str:pk>/', views.deleteTask, name='delete-task'),
    path('toggle-description/<str:pk>/', views.toggleDescription, name='toggle-description'),
]