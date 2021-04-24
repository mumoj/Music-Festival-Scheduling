from django.shortcuts import reverse, redirect

from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import(
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS
)
from rest_framework.response import Response
from rest_framework import status

from rest_auth.registration.views import RegisterView

from performances.models import Institution

from .models import (
    CustomUser, TeacherProfile,
    SponsorProfile, AdjudicatorProfile,
    DependentPerformerProfile,
    IndependentPerformerProfile
)

from .serializers import (
    TeacherProfileSerializer,
    SponsorProfileSerializer,
    AdjudicatorProfileSerializer,
    DependentPerformerProfileSerializer
)

from .permission_groups import set_heads_of_institutions_group


class CustomRegistrationView(RegisterView):
    """
    Customized Registration view for handling
    registration of users with various roles in the system
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Return the response once a user profile is created.
        response = Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers)

        if request.data['role'] == 'HEAD_OF_INSTITUTION':
            user.groups.add(set_heads_of_institutions_group())
            Institution.objects.create(head_of_institution=user)
            return response

        elif request.data['role'] == 'DEPENDENT_PERFORMER':
            dependent_performer_profile = DependentPerformerProfile. \
                objects.create(user=user)
            dependent_performer_profile.save()
            return response

        elif request.data['role'] == 'SPONSOR':
            sponsor_profile = SponsorProfile.objects.create(user=user)
            sponsor_profile.save()
            return response

        else:
            pass


class IsOwnerOrReadOnly(BasePermission):
    """Custom permission"""
    message = 'Updating of account details restricted to account owner'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class AddSponsorProfile(RetrieveUpdateAPIView):
    """
    Once registered, a sponsor has to update their profile details
    as they are germane to their role in the system.
    """
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'user'
    lookup_url_kwarg = 'sponsor'


class AddDependentPerformerProfile(RetrieveUpdateAPIView):
    """
    Once registered, a dependent performer has to update their profile details
    as they are germane to their role in the system.
    """
    queryset = DependentPerformerProfile.objects.all()
    serializer_class = DependentPerformerProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'user'
    lookup_url_kwarg = 'dependent_performer'
