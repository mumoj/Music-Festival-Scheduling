from pprint import pprint
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse
from accounts.permission_groups import HEADS_OF_INSTITUTION_GROUP
from accounts.models import (
    SponsorProfile,
    DependentPerformerProfile,
    CustomUser)
from performances.models import Institution
from django.contrib.auth.models import Group


# class DependentPerformerRegistrationAndProfileViewTests(APITestCase):
#     """
#     Test how dependent performer registration is handled by the system.
#     """
#     def test_dependent_performer_registration(self):
#         """
#         Test creation of the dependent performer profile.
#         """
#         url = reverse('accounts:register')
#         data = {
#             'first_name': 'John',
#             'middle_name': 'Mlachake',
#             'last_name': 'Doe',
#             'email': 'mlachake@gmail.com',
#             'role': 'DEPENDENT_PERFORMER',
#             'password1': '1234',
#             'password2': '1234',
#         }
#         self.client.post(url, data, format='json')
#         self.assertIsInstance(DependentPerformerProfile.objects.get(
#             user__email=data['email']), DependentPerformerProfile)

class HeadOfInstitutionRegistrationTest(APITestCase):
    """
    Test how an head of institution is registered in the system
    """

    def setUp(self) -> None:
        """"""
        self.registration_url = reverse('accounts:register')
        self.data = {
            'first_name': 'John',
            'middle_name': 'Mlachake',
            'last_name': 'Doe',
            'email': 'mlachake@gmail.com',
            'role': 'HEAD_OF_INSTITUTION',
            'password1': '1234',
            'password2': '1234',
        }

    def test_creation_of_an_institution_instance_on_registration(self):
         pass


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
            user__email=self.data['email']), SponsorProfile)

    def test_add_sponsor_profile_view(self):
        """
        Test sponsors are authenticated and are adding their own profile instances.
        """
        self.user = CustomUser.objects.get(email=self.data['email'])
        self.client.login(email=self.user.email, password=self.data['password1'])

        update_url = reverse('accounts:update-sponsor', kwargs={'sponsor': self.user.pk})
        response = self.client.put(update_url, {"payment_method": "PAYPAL"}, format='json')
        self.assertEqual(response.status_code, 200)
