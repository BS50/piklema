from rest_framework.response import Response
from piklema.serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelView(viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"]
        )
        return Response(UserSerializer(user).data)

