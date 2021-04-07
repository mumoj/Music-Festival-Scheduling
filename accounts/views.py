from django.shortcuts import reverse, redirect

from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView)
from rest_framework.response import Response
from rest_framework import status

from rest_auth.registration.views import RegisterView

from .models import (
    CustomUser, TeacherProfile,
    SponsorProfile, AdjudicatorProfile,
    DependentPerformerProfile,
    IndependentPerformerProfile)

from .serializers import (
    TeacherProfileSerializer,
    SponsorProfileSerializer,
    AdjudicatorProfileSerializer,
    DependentPerformerProfileSerializer)

from .group_permissions import HEADS_OF_INSTITUTION_GROUP


class CustomRegisterView(RegisterView):
    """
    Customized Register view for handling
    registration of users with various roles in the system
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        if request.data['role'] == 'SPONSOR':
            sponsor_profile = SponsorProfile.objects.create(user=user)
            sponsor_profile.save()
            return redirect(reverse(
                'accounts:register-sponsor',
                kwargs={'sponsor_profile_pk': sponsor_profile.pk})
            )

        elif request.data['role'] == 'DEPENDENT_PERFORMER':
            dependent_performer_profile = DependentPerformerProfile. \
                objects.create(user=user)
            dependent_performer_profile.save()
            return redirect(reverse(
                'accounts:register-dependent-performer',
                kwargs={'dependent_performer_profile_pk':
                            dependent_performer_profile.pk})
            )

        elif request.data['role'] == 'HEAD_OF_INSTITUTION':
            user.groups.add(HEADS_OF_INSTITUTION_GROUP)
            return redirect(reverse(
                'performances:register-institutions',
                kwargs={'head_of_institution': user})
            )

        else:
            headers = self.get_success_headers(serializer.data)
            return Response(
                self.get_response_data(user),
                status=status.HTTP_201_CREATED,
                headers=headers
            )


class RegisterSponsorProfile(RetrieveUpdateAPIView):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'sponsor_profile_pk'


class RegisterDependentPerformerProfile(RetrieveUpdateAPIView):
    queryset = DependentPerformerProfile.objects.all()
    serializer_class = DependentPerformerProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'dependent_performer_profile_pk'
