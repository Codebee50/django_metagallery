from rest_framework import serializers
from accounts.models import UserAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields= '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with that email already exits")
        return value
    
    def validate_username(self, value):
        print('validating username')
        if UserAccount.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists")
        return value