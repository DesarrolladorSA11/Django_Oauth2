import base64
import hashlib
import random
import string

import requests
from decouple import config
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import generics, permissions

from users.models import User
from users.serializers import GroupSerializer, UserSerializer

admin.autodiscover()


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ["groups"]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


""" OAUTH2 """


# Generate code challenge & code verifier
def generate_pkce_pair():
    code_verifier = "".join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(random.randint(43, 128))
    )
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    )
    return code_verifier, code_challenge


# Redirect
def authorize_request(request):
    try:
        client_id = config("CLIENT_ID")
        redirect_uri = config("REDIRECT_URI")

        code_verifier, code_challenge = generate_pkce_pair()
        request.session["code_verifier"] = code_verifier
        request.session["client_id"] = client_id
        request.session["redirect_uri"] = redirect_uri

        authorization_url = f"http://190.0.2.186:3000/o/authorize/?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&code_challenge={code_challenge}&code_challenge_method=S256"
        return render(
            request,
            "oauth/authorization.html",
            {"authorization_url": authorization_url},
        )

    except Exception as error:
        print("ERROR", str(error))
        return JsonResponse(
            {"success": False, "message": "Cliente OAuth no válido"}, status=400
        )


def oauth_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse(
            {"success": False, "message": "Código de autorización no recibido"},
            status=400,
        )

    client_id = request.session.get("client_id")
    redirect_uri = request.session.get("redirect_uri")
    code_verifier = request.session.get("code_verifier")

    if not client_id or not redirect_uri or not code_verifier:
        return JsonResponse(
            {"success": False, "message": "Sesión expirada o inválida"}, status=400
        )

    token_url = f"{settings.OAUTH2_PROVIDER['TOKEN_URL']}"

    # Data to sent. for token
    data = {
        "client_id": client_id,
        "client_secret": config("CLIENT_SECRET"),
        "code": code,
        "code_verifier": code_verifier,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    # Send data
    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        request.session["access_token"] = token_data.get("access_token")
        request.session["refresh_token"] = token_data.get("refresh_token")
        return JsonResponse(
            {"success": True, "message": "Token recibido", "data": token_data}
        )

    return JsonResponse(response.json(), status=response.status_code)
