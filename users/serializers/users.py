from rest_framework import serializers
from rest_framework.exceptions import ParseError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from events.serializers.common import EventListSerializer


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "is_organizer")

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                "Пользователь с такой почтой уже зарегестрирован.")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("old_password", "new_password")

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop("old_password")
        new_password = attrs.get("new_password")
        if not user.check_password(old_password):
            raise ParseError("Проверьте правильность текущего пароля")
        if old_password == new_password:
            raise ParseError("Новый пароль совпадает со старым паролем")
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("new_password")
        instance.set_password(password)
        instance.save()
        return instance


class UserSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'phone_number',
            "ava",
        )


class MeSerializer(serializers.ModelSerializer):
    events = EventListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "is_organizer",
            "ava",
            "about",
            "events",
        )
