from django.test import TestCase
from accounts.models import CustomUser


class CustomUserModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
            email='normal@gmail.com',
            first_name='Naby',
            middle_name='Deco',
            last_name='Keita'

        )

    def setUp(self) -> None:
        self.custom_user = CustomUser.objects.get(email='normal@gmail.com')

    def test_long_name(self):
        self.assertEqual(self.custom_user.get_long_name(), 'Naby Deco Keita')

    def test_get_short_name(self):
        self.assertEqual(self.custom_user.get_short_name(), 'Naby')

    def test__str__(self):
        self.assertEqual(self.custom_user.__str__(), 'normal@gmail.com')








