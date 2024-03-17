import pytz
from django.test import TestCase
from datetime import datetime
from mixer.backend.django import mixer

from piklema.device_data_validator import DeviceDataValidator, DeviceNotFoundException, TagValueException, \
    TagNotFoundException, DeviceData
from piklema.models import Device, Tag


class DeviceDataValidatorTestCase(TestCase):
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.device_1 = mixer.blend(Device)
        self.device_2 = mixer.blend(Device)
        self.tag_1 = mixer.blend(Tag, name="tag_1", ratio=0.5, min=-150, max=150, device=self.device_1)
        self.tag_2 = mixer.blend(Tag, name="tag_2", ratio=0.25, min=-100, max=100, device=self.device_1)

        self.tag_3 = mixer.blend(Tag, name="tag_3", ratio=0.6, min=-120, max=120, device=self.device_2)

    def test_validate_success(self):
        data_succses = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": self.device_1.pk,
            "version": "5.8",
            "tag_values": [{"name": "tag_1", "value": 50}, {"name": "tag_2", "value": 30}]
        }
        try:
            DeviceDataValidator.validate(DeviceData(**data_succses))
        except:
            self.assertTrue(False)

    def test_validate_device_error(self):
        data_device_error = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": 100000,
            "version": "5.8",
            "tag_values": [{"name": "tag_1", "value": 50}, {"name": "tag_2", "value": 30}]
        }
        with self.assertRaises(DeviceNotFoundException):
            DeviceDataValidator.validate(DeviceData(**data_device_error))

    def test_validate_tag_error_0(self):
        data_tag_error_0 = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": self.device_1.pk,
            "version": "5.8",
            "tag_values": [{"name": "tag_3", "value": 50}, {"name": "tag_2", "value": 30}]
        }
        with self.assertRaises(TagNotFoundException):
            DeviceDataValidator.validate(DeviceData(**data_tag_error_0))

    def test_validate_tag_error_1(self):
        data_tag_error_1 = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": self.device_1.pk,
            "version": "5.8",
            "tag_values": [{"name": "tag_1", "value": 50}, {"name": "tag_2", "value": 30}, {"name": "tag_3", "value": 25}]
        }
        with self.assertRaises(TagNotFoundException):
            DeviceDataValidator.validate(DeviceData(**data_tag_error_1))

    def test_validate_tag_value_error(self):
        data_tag_value_error = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": self.device_1.pk,
            "version": "5.8",
            "tag_values": [{"name": "tag_1", "value": 500}, {"name": "tag_2", "value": 30}]
        }
        with self.assertRaises(TagValueException):
            DeviceDataValidator.validate(DeviceData(**data_tag_value_error))
