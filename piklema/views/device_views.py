from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from piklema.models import Device, TagValue
from piklema.serializers import DeviceSerializer, TagValueSerializer


class DeviceModelView(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=["get"])
    def tag_values(self, request, pk):
        try:
            device = Device.objects.get(pk=pk)
            device_data = DeviceSerializer(device).data

            tag_value = TagValue.objects.filter(tag__device_id=pk).order_by("-timestamp").first()
            if tag_value is None:
                raise ValidationError(f"No tag_values for device with id: {pk}")
            tag_value_list = TagValue.objects.filter(timestamp=tag_value.timestamp, tag__device_id=pk)

            tag_value_list_data = TagValueSerializer(tag_value_list, many=True).data
            device_data["tag_value"] = tag_value_list_data

            return Response(device_data)
        except Device.DoesNotExist:
            raise ValidationError
