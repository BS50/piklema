from django.test import TestCase
from mixer.backend.django import mixer
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewTestCase(TestCase):
    LIST_URL = "user-list"
    def setUp(self):
        self.init_data()

    def init_data(self):
        self.user_0 = mixer.blend(User)
        self.user_1 = mixer.blend(User)

    def test_get(self):
        response = self.client.get(reverse(self.LIST_URL))
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)


    def test_add(self):
        data = {"username": "Alex", "email": "alex@gmail.com", "password": "12345"}
        response = self.client.post(reverse(self.LIST_URL), data, format="json", content_type='application/json')

        response_data = response.json()
        user = User.objects.get(pk=response_data["id"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data["id"], user.pk)



