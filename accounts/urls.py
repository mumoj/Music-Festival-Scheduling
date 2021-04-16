from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_auth.views import LoginView, LogoutView
from .views import (
    CustomRegistrationView,
    RegisterSponsorProfile,
    RegisterDependentPerformerProfile)

app_name = 'accounts'
urlpatterns = [
    path('accounts-confirm-email/<str:key>/',
         ConfirmEmailView.as_view()),

    path('register/', CustomRegistrationView.as_view(),
         name='register'),
    path('register/sponsor/<int:sponsor_profile_pk>/',
         RegisterSponsorProfile.as_view(),
         name='register-sponsor'),
    path('register/dependent_performer/<int:dependent_performer_profile_pk>/',
         RegisterDependentPerformerProfile.as_view(),
         name='register-dependent-performer'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('accounts-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^accounts-confirm-email/(?P<key>[-:\w]+)/$',
            VerifyEmailView.as_view(), name='account_confirm_email'),

    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
]
