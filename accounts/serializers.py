from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists

from rest_framework import serializers

from rest_auth.serializers import PasswordResetSerializer

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import (
    TeacherProfile,
    SponsorProfile,
    AdjudicatorProfile,
    DependentPerformerProfile,
    IndependentPerformerProfile,
    CustomUser)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    """
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        )

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'middle_name': self.validated_data.get('middle_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    def create(self, **validated_data):

        user = get_user_model()
        print(validated_data)
        validated_data = validated_data.pop('validated_data')
        print(validated_data)
        user = user.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name')
        )
        user.set_password(user.password)
        return user

    def update(self, instance, validated_data):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user


class DependentPerformerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DependentPerformerProfile
        fields = ('institution', 'performance_class', 'sponsor',)


class IndependentPerformerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = IndependentPerformerProfile


class TeacherProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = ('institution', 'performances')


class SponsorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorProfile
        fields = ('payment_method',)


class AdjudicatorProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=True)

    class Meta:
        model = AdjudicatorProfile
        fields = ('user', 'national_id',)


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'subject_template_name': 'email/password_reset_key_subject.txt',
            'email_template_name': 'email/password_reset_key_message.txt',
            'html_email_template_name': 'email/password_reset_email.html',
        }
