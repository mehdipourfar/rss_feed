from rest_framework.test import APITestCase

from .factories import UserFactory


class UserViewSetTestCase(APITestCase):
    def test_login(self):
        username = 'abcd'
        password = 'FS2322rfR@'

        login_api = '/api/users/login/'

        # create user
        response = self.client.post(
            login_api,
            {'username': username, 'password': password},
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            set(response.json().keys()),
            {'user', 'token'}
        )

        # login with invalid password
        response = self.client.post(
            login_api,
            {'username': username, 'password': '123'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {'error': "Invalid username or password"}
        )

        # login with correct password
        response = self.client.post(
            login_api,
            {'username': username, 'password': password},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json().keys()),
            {'user', 'token'}
        )

    def test_me(self):
        me_api = '/api/users/me/'
        response = self.client.get(me_api)
        self.assertEqual(response.status_code, 401)
        user = UserFactory()
        self.client.force_authenticate(user=user)

        response = self.client.get(me_api)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'username': user.username, 'id': user.id}
        )
