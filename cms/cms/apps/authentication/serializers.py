from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth.hashers import make_password

from cms.apps.authentication import models
from cms.apps.authentication.validator import SanityValidator


class CustomUserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = models.CustomUser
        fields = ['email', 'phone', 'address', 'city', 'state', 'country', 'pincode',
                  'password', 'first_name', 'last_name', 'fullname']
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'write_only': True},
                        'last_name': {'write_only': True}}

    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_password(self, value):
        validator = SanityValidator()
        validator.validate(password=value)
        return value

    def save(self, **kwargs):
        if not self.validated_data.get('password'):
            raise exceptions.ValidationError("password is required field.")

        self.validated_data['password'] = make_password(self.validated_data['password'])

        return super().save(**kwargs)
