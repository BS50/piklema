from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from piklema.models import Tag


class TagViewTestCase(TestCase):
    LIST_URL = "tag-list"
    DETAIL_URL = "tag-detail"
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.tag_0 = mixer.blend(Tag, name="tag_0")
        self.tag_1 = mixer.blend(Tag, name="tag_1")

    def test_get(self):
        response = self.client.get(reverse(self.LIST_URL))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

    def test_get_id(self):
        tag_id = self.tag_0.pk
        response = self.client.get(reverse(self.DETAIL_URL, kwargs={"pk": tag_id}))
        response_data = response.json()
        tag = Tag.objects.get(pk=tag_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], tag_id)
        self.assertEqual(response_data["id"], tag.pk)


    def test_add(self):
        data = {"name": "tag_2", "device_id": self.tag_0.device_id, "ratio": 0.5, "min": -150, "max": 150}
        response = self.client.post(reverse(self.LIST_URL), data, format="json", content_type='application/json')

        response_data = response.json()
        tag = Tag.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data["id"], tag.pk)


    def test_update(self):
        name = "tag_8"
        device_id = self.tag_0.device_id
        data = {"device_id": device_id, "name": name, "ratio": 0.5, "min": -150, "max": 150}
        response = self.client.put(
            reverse(self.DETAIL_URL, kwargs={"pk": self.tag_0.pk}), data, format="json", content_type='application/json'
        )

        response_data = response.json()
        tag = Tag.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], tag.pk)
        self.assertEqual(response_data["device"]["id"], device_id)

    def test_remove(self):
        self.client.delete(reverse(self.DETAIL_URL, kwargs={"pk": self.tag_0.pk}))
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(pk=self.tag_0.pk)