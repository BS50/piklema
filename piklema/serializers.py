from rest_framework import serializers
from piklema.models import Tag, Device, TagValue
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='user')

    class Meta:
        model = Device
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Device.objects.all(), source='device')

    class Meta:
        model = Tag
        fields = "__all__"

class TagValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagValue
        fields = "__all__"
