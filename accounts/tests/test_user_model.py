from datetime import date

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from accounts.models import Address
from tickets.tests.factories import create_user

User = get_user_model()


class UserModelTests(TestCase):
    def test_can_create_user_with_date_of_birth(self):
        user = create_user(
            username="profileuser",
            email="profile@example.com",
            date_of_birth=date(1998, 5, 20),
        )

        self.assertEqual(user.email, "profile@example.com")
        self.assertEqual(user.date_of_birth, date(1998, 5, 20))

    def test_email_must_be_unique(self):
        create_user(
            username="first",
            email="shared@example.com",
        )

        with self.assertRaises(IntegrityError):
            create_user(
                username="second",
                email="shared@example.com",
            )

    def test_email_is_required(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="no-email",
                password="testpass123",
                email="",
            )

    def test_date_of_birth_is_optional(self):
        user = User.objects.create_user(
            username="no-dob",
            email="no-dob@example.com",
            password="testpass123",
        )

        self.assertIsNone(user.date_of_birth)


class AddressModelTests(TestCase):
    def test_user_can_have_an_address(self):
        user = create_user(
            username="address-user",
            email="address-user@example.com",
            address_data={
                "house_name_or_number": "12",
                "street": "Test Street",
                "city": "Wolverhampton",
                "postcode": "WV1 1AA",
            },
        )

        self.assertEqual(user.address.house_name_or_number, "12")
        self.assertEqual(user.address.street, "Test Street")
        self.assertEqual(user.address.city, "Wolverhampton")
        self.assertEqual(user.address.postcode, "WV1 1AA")

    def test_address_is_optional(self):
        user = create_user(
            username="no-address",
            email="no-address@example.com",
        )

        self.assertFalse(Address.objects.filter(user=user).exists())

    def test_user_can_have_only_one_address(self):
        user = create_user(
            username="one-address",
            email="one-address@example.com",
            address_data={
                "house_name_or_number": "12",
                "street": "Test Street",
                "city": "Wolverhampton",
                "postcode": "WV1 1AA",
            },
        )

        with self.assertRaises(IntegrityError):
            Address.objects.create(
                user=user,
                house_name_or_number="14",
                street="Another Street",
                city="Wolverhampton",
                postcode="WV2 2BB",
            )

    def test_address_is_deleted_with_user(self):
        user = create_user(
            username="delete-address",
            email="delete-address@example.com",
            address_data={
                "house_name_or_number": "12",
                "street": "Test Street",
                "city": "Wolverhampton",
                "postcode": "WV1 1AA",
            },
        )

        address_id = user.address.id
        user.delete()

        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_address_string_representation(self):
        user = create_user(
            username="address-str",
            email="address-str@example.com",
            address_data={
                "house_name_or_number": "12",
                "street": "Test Street",
                "city": "Wolverhampton",
                "postcode": "WV1 1AA",
            },
        )

        self.assertEqual(
            str(user.address),
            "12, Test Street, Wolverhampton, WV1 1AA",
        )