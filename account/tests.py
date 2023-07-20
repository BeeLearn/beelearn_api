from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def create_user_token_return(self):
        response = self.client.post(
            "/api/account/users/",
            {
                "username": "test_user_unique_1",
                "email": "test_user_unique_1@gmail.com",
                "password": "test_user_unique_1",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data: dict = response.json()

        self.assertIsInstance(data, dict)

    def list_all_user(self):
        response = self.client.get("/api/account/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)

    def retrieve_current_user(self):
        response = self.client.get(f"/api/account/users/?uid={self.uid}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["uid"], self.uid)

    def update_current_user(self):
        pass

    def delete_current_user(self):
        pass
