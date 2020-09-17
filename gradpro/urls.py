from django.urls import path
from gradpro import views

app_name = 'gradpro'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('questionnaire2/', views.questionnaire2, name='questionnaire2'),
    path('questionnaire3/', views.questionnaire3, name='questionnaire3'),
    path('communication/', views.communication, name='communication'),
    path('communication2/', views.communication2, name='communication2'),
    path('communication3/', views.communication3, name='communication3'),
    path('adaptability/', views.adaptability, name='adaptability'),
    path('adaptability2/', views.adaptability2, name='adaptability2'),
    path('adaptability3/', views.adaptability3, name='adaptability3'),
    path('adaptability4/', views.adaptability4, name='adaptability4'),
    path('adaptability5/', views.adaptability5, name='adaptability5'),
]