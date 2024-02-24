from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar', 'payment_history', 'password']

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


