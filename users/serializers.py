from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(
        allow_empty=False, many=True, read_only=True
    )
    subscriptions = serializers.PrimaryKeyRelatedField(
        allow_empty=False, many=True, read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "karma",
            "posts",
            "friends",
            "subscriptions",
        )
        read_only_fields = (
            "karma",
            "friends",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance
