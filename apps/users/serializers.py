from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Поля твоей модели для фитнеса (добавь свои, если нужно)
        fields = ('username', 'email', 'password', 'weight', 'height')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            weight=validated_data.get('weight', None),
            height=validated_data.get('height', None),
        )
        return user