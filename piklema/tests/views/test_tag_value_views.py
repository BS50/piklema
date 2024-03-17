from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from piklema.models import TagValue


class TagValueViewTestCase(TestCase):
    LIST_URL = "tag-value-list"
    DETAIL_URL = "tag-value-detail"
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.tag_value_0 = mixer.blend(TagValue, name="tag_0")
        self.tag_value_1 = mixer.blend(TagValue, name="tag_1")

    def test_get(self):
        response = self.client.get(reverse(self.LIST_URL))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

    def test_get_id(self):
        tag_value_id = self.tag_value_0.pk
        response = self.client.get(reverse(self.DETAIL_URL, kwargs={"pk": tag_value_id}))
        response_data = response.json()
        tag_value = TagValue.objects.get(pk=tag_value_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], tag_value_id)
        self.assertEqual(response_data["id"], tag_value.pk)
