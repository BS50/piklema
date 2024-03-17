import logging
from datetime import datetime
from django.test import TestCase
from mixer.backend.django import mixer
import pytz

from piklema.device_data_validator import DeviceData
from piklema.models import Device, Tag, TagValue
from processor_script import convert_data, create_tag_values


class ProcessorTestCase(TestCase):
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.data = {
            "timestamp": str(datetime.now(pytz.timezone("Europe/Moscow"))),
            "device_id": 1,
            "version": "5.8",
            "tag_1": 50,
            "tag_2": 30
        }
        self.converted_data = {
            "timestamp": self.data["timestamp"],
            "device_id": 1,
            "version": "5.8",
            "tag_values": [{"name": "tag_1", "value": 50}, {"name": "tag_2", "value": 30}]

        }

        self.device_1 = mixer.blend(Device)

        self.tag_1 = mixer.blend(Tag, name="tag_1", ratio=0.5, min=-150, max=150, device=self.device_1)
        self.tag_2 = mixer.blend(Tag, name="tag_2", ratio=0.25, min=-100, max=100, device=self.device_1)

    def test_convert_data(self):
        device_data = convert_data(self.data)
        self.assertEqual(device_data.device_id, self.data["device_id"])
        self.assertEqual(device_data.version, self.data["version"])
        self.assertEqual(len(device_data.tag_values), 2)

    def test_create_tag_value(self):
        create_tag_values(logging.getLogger(), DeviceData(**self.converted_data))
        tag_value = TagValue.objects.get(tag_id=self.tag_1.pk)
        tz = pytz.timezone("Europe/Moscow")
        time_with_time_zone = tz.normalize(tag_value.timestamp.astimezone(tz))
        format_date = time_with_time_zone.strftime('%Y-%m-%d %H:%M:%S.%f+03:00')
        self.assertEqual(self.converted_data["timestamp"], format_date)
        self.assertEqual(self.converted_data["version"], tag_value.version)
