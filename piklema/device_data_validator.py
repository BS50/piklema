from piklema.models import Device, Tag
from django.core.exceptions import ObjectDoesNotExist
from pydantic import BaseModel


class TagValue(BaseModel):
    name: str
    value: int


class DeviceData(BaseModel):
    device_id: int
    timestamp: str
    version: str
    tag_values: list[TagValue]


class DeviceNotFoundException(Exception):
    pass


class TagNotFoundException(Exception):
    pass


class TagValueException(Exception):
    pass


class DeviceDataValidator:
    @staticmethod
    def validate(device_data: DeviceData) -> None:
        DeviceDataValidator.__validate_device(device_data.device_id)
        DeviceDataValidator.__validate_tag(device_data.device_id, device_data.tag_values)

    @staticmethod
    def __validate_device(device_id: int) -> None:
        try:
            Device.objects.get(pk=device_id)
        except ObjectDoesNotExist:
            raise DeviceNotFoundException("Device not found")

    @staticmethod
    def __validate_tag(device_id: int, tag_values: list[TagValue]) -> None:
        for tag_obj in tag_values:
            try:
                tag = Tag.objects.get(device_id=device_id, name=tag_obj.name)
                if not tag.min < tag_obj.value * tag.ratio < tag.max:
                    raise TagValueException("Tag value is not correct")
            except ObjectDoesNotExist:
                raise TagNotFoundException("Tag not found")
