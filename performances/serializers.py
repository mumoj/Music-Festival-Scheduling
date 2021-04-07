from rest_framework import serializers
from .models import Institution


class InstitutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institution
        fields = (
            'name',
            'institution_type',
            'zone',
            'sub_county',
            'county',
            'region'
        )
