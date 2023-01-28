from django.urls import path
from app import views

urlpatterns = [
    path('animal/',views.AnimalView.as_view()),
    path('animal/<pk>/',views.AnimalDetails.as_view()), 
    path('register/',views.RegisterAPI.as_view()),
    path('login/',views.LoginAPI.as_view()),
    path('createAnimal/',views.AnimalCreateAPI.as_view()),
                                         
                                         
                                               
]