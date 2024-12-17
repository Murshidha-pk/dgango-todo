from django.urls import path

from api import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[

    path('signup/',views.UserCreationView.as_view()),

    path('todos/',views.TodoListCreateView.as_view()),

    path('todos/<int:pk>/',views.TodoRetrieveUpdateDestroyView.as_view()),

    path('token/',ObtainAuthToken.as_view()),

    

    




]