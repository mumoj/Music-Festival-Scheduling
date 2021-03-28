from django.shortcuts import render
from rest_framework import generics
from .serializers import InstitutionSerializer
from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoModelPermissions,
    BasePermission
)
from .models import (
    Institution,
    Class,
    Performance
)


# Create your views here.
class HeadOfInstitutionPermission(BasePermission):
    message = 'Updating of details  and deregistration of institution' \
              '  restricted to Head of Institution Only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.head_of_institution == request.user


class RegisterInstitutions(generics.CreateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [DjangoModelPermissions, HeadOfInstitutionPermission]









