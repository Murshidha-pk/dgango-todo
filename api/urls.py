from django.urls import path

from api import views

urlpatterns=[

    path('signup/',views.UserCreationView.as_view()),

    path('todos/',views.TodoListCreateView.as_view()),

    path('todos/<int:pk>/',views.TodoRetrieveUpdateDestroyView.as_view()),

    




]