from model_bakery import baker
from rest_framework.test import APITestCase
from pprint import pprint

from django.urls import reverse

from accounts.permission_groups import heads_of_institutions_group
from accounts.models import (
    TeacherProfile,
    SponsorProfile,
    DependentPerformerProfile,
    CustomUser)

from performances.models import Institution


class HeadOfInstitutionRegistrationTest(APITestCase):
    """
    Test how an head of institution is registered in the system
    """

    def setUp(self) -> None:
        """"""
        self.registration_url = reverse('accounts:register')
        self.user_data = {
            'first_name': 'John',
            'middle_name': 'Mlachake',
            'last_name': 'Doe',
            'email': 'mlachake@gmail.com',
            'role': 'HEAD_OF_INSTITUTION',
            'password1': '1234',
            'password2': '1234',
        }
        self.head_of_institution_group = heads_of_institutions_group()
        self.client.post(self.registration_url, self.user_data, format='json')
        self.institution = Institution.objects.get(
            head_of_institution__email=self.user_data['email'])

    def test_creation_of_an_institution_instance_on_registration(self):
        self.assertIsInstance(self.institution, Institution)


class DependentPerformerRegistrationAndProfileViewTests(APITestCase):
    """
    Test how sponsor registration is handled by the system.
    """

    def setUp(self) -> None:
        self.registration_url = reverse('accounts:register')
        self.data = {
            'first_name': 'John',
            'middle_name': 'Mlachake',
            'last_name': 'Doe',
            'email': 'mlachake@gmail.com',
            'role': 'DEPENDENT_PERFORMER',
            'password1': '1234',
            'password2': '1234',
        }
        self.client.post(self.registration_url, self.data, format='json')
        self.dependent_performer_profile = DependentPerformerProfile.objects.get(
            user__email=self.data['email'])

    def test_a_dependent_performer_profile_instance_is_created_on_registration(self):
        self.assertIsInstance(self.dependent_performer_profile, DependentPerformerProfile)

    def test_add_dependent_profile_view(self):
        """
        Test sponsors are authenticated and
        they and they only are able to add their own profile instances.
        """
        self.user = CustomUser.objects.get(email=self.data['email'])
        self.client.login(email=self.user.email, password=1234)
        self.performance = baker.make('performances.Performance')
        self.institution = baker.make('performances.Institution')

        update_url = reverse(
            'accounts:update-dependent_performer',
            kwargs={'dependent_performer': self.dependent_performer_profile.pk})

        response = self.client.put(
            update_url,
            {'institution': self.institution.pk, 'performance': [self.performance.pk]},
            format='json')
        pprint(response.__dict__)
        self.assertEqual(response.status_code, 200)


class SponsorRegistrationAndProfileViewTests(APITestCase):
    """
    Test how sponsor registration is handled by the system.
    """

    def setUp(self) -> None:
        self.registration_url = reverse('accounts:register')
        self.data = {
            'first_name': 'John',
            'middle_name': 'Mlachake',
            'last_name': 'Doe',
            'email': 'mlachake@gmail.com',
            'role': 'SPONSOR',
            'password1': '1234',
            'password2': '1234',
        }
        self.client.post(self.registration_url, self.data, format='json')

    def test_sponsor_profile_instance_is_created_on_registration(self):
        self.assertIsInstance(SponsorProfile.objects.get(
            user__email=self.data['email']), SponsorProfile
        )

    def test_add_sponsor_profile_view(self):
        """
        Test sponsors are authenticated and that they are adding their own profile instances.
        """
        self.user = CustomUser.objects.get(email=self.data['email'])
        self.client.login(email=self.user.email, password=self.data['password1'])

        update_url = reverse(
            'accounts:update-sponsor',
            kwargs={'sponsor': self.user.pk})
        response = self.client.put(
            update_url,
            {"payment_method": "PAYPAL"},
            format='json')
        self.assertEqual(response.status_code, 200)


class TeacherRegistrationAndProfileViewTests(APITestCase):
    """
    Test how teacher registration is handled by the system.
    """

    def setUp(self) -> None:
        self.registration_url = reverse('accounts:register')
        self.data = {
            'first_name': 'Joe',
            'middle_name': 'Mlachake',
            'last_name': 'Doe',
            'email': 'mlachakejoe@gmail.com',
            'role': 'TEACHER',
            'password1': '1234',
            'password2': '1234',
        }
        self.client.post(self.registration_url, self.data, format='json')

    def test_teacher_profile_instance_is_created_on_registration(self):
        self.assertIsInstance(TeacherProfile.objects.get(
            user__email=self.data['email']), TeacherProfile
        )

    def test_add_teacher_profile_view(self):
        """
        Test teachers are authenticated when adding their profiles
         and that they are adding their own profile instances.
        """
        self.user = CustomUser.objects.get(email=self.data['email'])
        self.client.login(email=self.user.email, password=self.data['password1'])
        self.performance = baker.make('performances.Performance')
        self.institution = baker.make('performances.Institution')

        update_url = reverse(
            'accounts:update-teacher',
            kwargs={'teacher': self.user.pk})
        response = self.client.put(
            update_url,
            {"institution": self.institution.pk, "performances": [self.performance.pk]},
            format='json')
        self.assertEqual(response.status_code, 200)
