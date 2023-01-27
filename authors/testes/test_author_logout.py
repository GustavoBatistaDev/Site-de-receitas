from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_superuser(
            username='myuser', password='mypass_pass'
        )

        self.client.login(username='myuser', password='mypass_pass') # noqa

        response = self.client.get(reverse('authors:logout'), follow=True)

        self.assertIn(
            'Click to logout button', response.content.decode('utf-8')
            )

    def test_another_user_request(self):
        User.objects.create_superuser(
            username='myuser', password='mypass_pass'
        )

        self.client.login(username='myuser', password='mypass_pass') # noqa

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={'username': 'anotherUser'}
            )

        print(response)

        self.assertIn(
            'Invalid logout user.', response.content.decode('utf-8')
            )

    def test_success_logout(self):
        User.objects.create_superuser(
            username='myuser', password='mypass_pass'
        )

        self.client.login(username='myuser', password='mypass_pass') # noqa

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={'username': 'myuser'}
        )

        print(response)
        self.assertIn(
            'Logout successfully.', response.content.decode('utf-8')
            )