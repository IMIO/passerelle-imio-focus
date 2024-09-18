import json

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests import session
from requests_oauthlib import OAuth2Session
from django.db import models
from passerelle.base.models import BaseResource
from passerelle.utils.api import endpoint
from django.conf import settings


class ConnectorFocus(BaseResource):
    """
    Connector FOCUS
    """

    api_description = "Connecteur pour FOCUS la plateforme de gestion de la Police"
    category = "Connecteurs iMio"

    class Meta:
        verbose_name = "Connecteur pour FOCUS"

    url_auth = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="URL d'authentification",
        help_text="URL d'authentification pour aller chercher le token",
    )

    client_id = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="Client ID",
        help_text="Client ID pour l'API",
    )

    client_secret = models.CharField(
        max_length=1024,
        blank=False,
        verbose_name="Client Secret",
        help_text="Mot de passe pour avoir le token de l'API",
    )

    url = models.CharField(
        max_length=128,
        blank=False,
        verbose_name="URL de l'instance",
        help_text="URL de l'instance FOCUS",
    )

    @property
    def session(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.url_auth,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return oauth

    def get_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=self.url_auth,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return token

    @endpoint(
        name="event",
        perm="can_access",
        methods=["post"],
        description="Créer un événement",
        long_description="Permet de créer un événement dans FOCUS",
        display_order=1,
        display_category="EVENEMENT",
        pattern="^create",
        example_pattern="create",
        parameters={
            "provider": {
                "description": "Fournisseur des données",
                "example_value": "iMio",
            },
        },
    )
    def create_event(
        self,
        request,
        provider="iMio",
    ):

        url = requests.compat.urljoin(self.url, f"oo-app/v1/happenings/{provider}")
        headers = {"Content-Type": "application/json"}

        response = self.session.post(url=url, headers=headers, data=json.dumps({}))
        response.raise_for_status()

        return response.json()

    @endpoint(
        name="event",
        perm="can_access",
        methods=["get"],
        description="Get un événement",
        long_description="Permet de récupérer un événement dans FOCUS",
        display_order=2,
        display_category="EVENEMENT",
        pattern="^get",
        example_pattern="get",
        parameters={
            "provider": {
                "description": "Fournisseur des données",
                "example_value": "iMio",
            },
            "external_id": {
                "description": "Identifiant externe",
                "example_value": "123456",
            },
        },
    )
    def get_fiche_membre(self, request, provider="iMio", external_id=None):
        url = requests.compat.urljoin(self.url, f"oo-app/v1/happenings/{provider}/{external_id}")
        headers = {"Content-Type": "application/json"}

        response = self.session.get(url=url, headers=headers)
        response.raise_for_status()

        return response.json()
