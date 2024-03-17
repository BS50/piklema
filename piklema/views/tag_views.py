from rest_framework import viewsets
from piklema.models import Tag
from piklema.serializers import TagSerializer


class TagModelView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
