from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'date_of_birth',
        ]
        read_only_fields = ['id']

    def validate_email(self, value):
        value = value.strip().lower()

        if not value:
            raise serializers.ValidationError(
                'Email address is required.'
            )

        return value

    def validate_username(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                'Username is required.'
            )

        return value

    def validate_password(self, value):
        validate_password(value)

        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth=validated_data.get('date_of_birth'),
        )
    

class MeSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = [
                "id",
                "username",
                "email",
                "date_of_birth",
            ]
            read_only_fields = fields