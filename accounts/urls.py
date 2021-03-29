from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomRegisterView, RegisterSponsorProfile,
                    RegisterDependentPerformerProfile)

app_name = 'accounts'
urlpatterns = [
    path('register/', CustomRegisterView.as_view(),
         name='register'),

    path('register/sponsor/<int:sponsor_profile_pk>/',
         RegisterSponsorProfile.as_view(),
         name='register-sponsor'),

    path('register/dependent_performer/<int:dependent_performer_profile_pk>/',
         RegisterDependentPerformerProfile.as_view(),
         name='register-dependent-performer')

]
