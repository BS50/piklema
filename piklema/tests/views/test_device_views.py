import pytz
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from piklema.models import Device, Tag, TagValue


class DeviceViewTestCase(TestCase):
    LIST_URL = "device-list"
    DETAIL_URL = "device-detail"
    TAG_VALUES_URL = "device-tag-values"
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.device_0 = mixer.blend(Device)
        self.device_1 = mixer.blend(Device)

        self.tag_0 = mixer.blend(Tag, device=self.device_0)
        self.tag_1 = mixer.blend(Tag, device=self.device_0)
        self.tag_2 = mixer.blend(Tag, device=self.device_1)
        self.tag_3 = mixer.blend(Tag, device=self.device_1)

        self.tag_value_0 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:15.104214+03:00", tag=self.tag_0)
        self.tag_value_1 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:15.104214+03:00", tag=self.tag_1)
        self.tag_value_3 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:30.104214+03:00", tag=self.tag_0)
        self.tag_value_4 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:30.104214+03:00", tag=self.tag_1)
        self.tag_value_5 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:40.104214+03:00", tag=self.tag_2)
        self.tag_value_6 = mixer.blend(TagValue, timestamp="2024-03-05 12:00:40.104214+03:00", tag=self.tag_3)

    def test_get(self):
        response = self.client.get(reverse(self.LIST_URL))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

    def test_get_id(self):
        device_id = self.device_0.pk
        response = self.client.get(reverse(self.DETAIL_URL, kwargs={"pk": device_id}))
        response_data = response.json()
        device = Device.objects.get(pk=device_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], device_id)
        self.assertEqual(response_data["id"], device.pk)

    def test_add(self):
        data = {"name": "device_2", "user_id": self.device_0.user_id}
        response = self.client.post(reverse(self.LIST_URL), data, format="json", content_type='application/json')
        response_data = response.json()
        device = Device.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], device.pk)

    def test_update(self):
        name = "device_8"
        user_id = self.device_1.user_id
        data = {"user_id": user_id, "name": name}
        response = self.client.put(
            reverse(self.DETAIL_URL, kwargs={"pk": self.device_0.pk}), data, format="json", content_type='application/json'
        )

        response_data = response.json()
        device = Device.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], device.pk)
        self.assertEqual(response_data["user"]["id"], user_id)

    def test_remove(self):
        self.client.delete(reverse(self.DETAIL_URL, kwargs={"pk": self.device_0.pk}))
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(pk=self.device_0.pk)

    def test_last_value(self):
        device_id = self.device_0.pk
        response = self.client.get(reverse(self.TAG_VALUES_URL, kwargs={"pk": device_id}))
        response_data = response.json()
        tag_value = TagValue.objects.filter(tag__device_id=device_id).order_by("-timestamp").first()
        tag_value_list = TagValue.objects.filter(timestamp=tag_value.timestamp, tag__device_id=device_id)

        self.assertEqual(response.status_code, 200)
        tz = pytz.timezone("Europe/Moscow")
        time_with_time_zone = tz.normalize(tag_value_list[0].timestamp.astimezone(tz))
        format_date = time_with_time_zone.strftime('%Y-%m-%dT%H:%M:%S.%f+03:00')
        self.assertEqual(response_data["tag_value"][0]["timestamp"], format_date)
