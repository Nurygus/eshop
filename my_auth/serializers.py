from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True, 'min_length': 5}
        }

    def validate(self, attrs):
        ModelClass = self.Meta.model
        email = attrs.get('email', '').strip().lower()

        if ModelClass.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email id already exists.')
        return attrs

    def create(self, validated_data):
        ModelClass = self.Meta.model
        user = ModelClass.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                "Please give both email and password.")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist.')

        user = User.objects.get(email=email)
        if not user.check_password(password):
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    expiry = serializers.DateTimeField()


class LogoutResponseSerializer(serializers.Serializer):
    """
    Empty logout response serializer
    """


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'id']
