from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomRegisterView, RegisterSponsorProfile

app_name = 'accounts'
urlpatterns = [
    path('register/', CustomRegisterView.as_view(),
         name='register'),
    path('register/sponsor/<int:sponsor_profile_pk>/', RegisterSponsorProfile.as_view()
         , name='register-sponsor')

]
