# serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'username', 'created_at', 'modified_at']
        extra_kwargs = {'password': {'write_only': True}}

class UserSignupSerializer(serializers.ModelSerializer):
    # Define the fields here
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=255, required=False)  # Add any other fields as needed
    
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'username']

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
            message = "User Created Successfully"
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
