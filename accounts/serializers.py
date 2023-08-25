from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class LoginSerializer(EmailSerializer, PasswordSerializer):
    pass