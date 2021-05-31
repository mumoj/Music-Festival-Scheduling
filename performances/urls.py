from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RegisterInstitutions,
    schedule_performances)

app_name = 'performances'
urlpatterns = [
    path('register-institution/<int:institution_pk>',
         RegisterInstitutions.as_view(),
         name='register-institution'),
    path('schedule-performances/<str:event>',
         schedule_performances, name='schedule-performances')
]
