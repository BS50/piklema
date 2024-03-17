from rest_framework import viewsets

from piklema.models import TagValue
from piklema.serializers import TagValueSerializer


class TagValueModelView(viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = TagValue.objects.all()
    serializer_class = TagValueSerializer
