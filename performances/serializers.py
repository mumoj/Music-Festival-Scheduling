from rest_framework import serializers
from .models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
    head_of_institution = serializers.ReadOnlyField(source='head_of_institution.__str__')

    class Meta:
        model = Institution
        fields = (
            'name',
            'head_of_institution',
            'institution_type',
            'zone',
            'sub_county',
            'county',
            'region'
        )
