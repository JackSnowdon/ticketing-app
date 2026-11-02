from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')
        self.valid_payload = {
            'username': 'demo_user',
            'email': 'demo@example.com',
            'password': 'StrongPassword123!',
            'date_of_birth': '1998-05-20',
        }

    def test_registration_returns_201_and_does_not_expose_password(self):
        response = self.client.post(
            self.url,
            self.valid_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'demo_user')
        self.assertEqual(response.data['email'], 'demo@example.com')
        self.assertNotIn('password', response.data)

        self.assertTrue(
            User.objects.filter(username='demo_user').exists()
        )

    def test_duplicate_email_is_rejected(self):
        self.client.post(self.url, self.valid_payload, format='json')

        duplicate_payload = {
            **self.valid_payload,
            'username': 'another_user',
        }

        response = self.client.post(
            self.url,
            duplicate_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_duplicate_username_is_rejected(self):
        self.client.post(self.url, self.valid_payload, format='json')

        duplicate_payload = {
            **self.valid_payload,
            'email': 'another@example.com',
        }

        response = self.client.post(
            self.url,
            duplicate_payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_empty_email_is_rejected(self):
        payload = {
            **self.valid_payload,
            'email': '   ',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_weak_password_is_rejected(self):
        payload = {
            **self.valid_payload,
            'password': 'password',
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)