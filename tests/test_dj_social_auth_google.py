from unittest import mock
import uuid

from allauth.socialaccount.models import SocialApp, SocialAccount
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITransactionTestCase


class GoogleLoginViewTestCase(APITransactionTestCase):
    def setUp(self):
        site = Site.objects.get(id=1)
        baker.make(SocialApp, provider="google", sites=[site])
        self.url = reverse("google_login")


    @mock.patch("allauth.socialaccount.providers.oauth2.client.OAuth2Client.get_access_token")
    @mock.patch("requests.get")
    def test_creates_new_user(self, mock_requests_get, mock_get_access_token):
        mock_get_access_token.return_value = {"access_token": "teste"}

        mock_response = mock.Mock()
        # Define response data from Google API
        expected_dict = {
            'id': uuid.uuid4(),
            'email': 'teste@teste.com',
            'verified_email': True,
            'given_name': 'Teste',
            'family_name': 'Da Silva',
        }

        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_requests_get.return_value = mock_response

        self.client.post(self.url, data={"code": "test"}, format="json")

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "teste")


    @mock.patch("allauth.socialaccount.providers.oauth2.client.OAuth2Client.get_access_token")
    @mock.patch("allauth.socialaccount.providers.google.views.requests.get")
    def test_returns_error_when_user_already_exists(self, mock_requests_get, mock_oauth_client):
        user = baker.make(User, email='teste@teste.com', first_name="teste", last_name="Da Silva")
        mock_oauth_client.return_value = {"access_token": "teste"}
        mock_response = mock.Mock()
        # Define response data from Google API
        expected_dict = {
            'id': '106071520986105119499',
            'email': user.email,
            'verified_email': True,
            'given_name': user.first_name,
            'family_name': user.last_name,
        }

        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_requests_get.return_value = mock_response
        self.client.post(self.url, data={"code": "test"}, format="json")

        self.assertEqual(User.objects.count(), 1)
        user.refresh_from_db()
        self.assertEqual(user.username, "teste")
        social_account = SocialAccount.objects.get(user__username=user.username)
        self.assertIsNotNone(social_account)
        self.assertEqual(social_account.user, user)

    @mock.patch("allauth.socialaccount.providers.oauth2.client.OAuth2Client.get_access_token")
    @mock.patch("allauth.socialaccount.providers.google.views.requests.get")
    def test_1(self, mock_requests_get, mock_oauth_client):
        baker.make(User,
            username="renato",
            email='renato@labcodes.com.br',
            first_name="Renato",
            last_name="Oliveira"
        )

        user2 = baker.make(User,
            username="lelis",
            email='lelis@labcodes.com.br',
            first_name="Renato",
            last_name="Lelis"
        )

        mock_oauth_client.return_value = {"access_token": "teste"}
        mock_response = mock.Mock()
        # Define response data from Google API
        expected_dict = {
            'id': '106071520986105119499',
            'email': user2.email,
            'verified_email': True,
            'given_name': "Renato",
            'family_name': "Lelis",
        }

        # Define response data for my Mock object
        mock_response.json.return_value = expected_dict
        mock_response.status_code = 200

        # Define response for the fake API
        mock_requests_get.return_value = mock_response
        self.client.post(self.url, data={"code": "test"}, format="json")

        user2.refresh_from_db()
        self.assertEquals(user2.username, "lelis")
