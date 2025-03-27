from django.urls import path

from .views import (  # get_access_token,; authorize_request,; oauth_callback,
    CustomAuthorizationView,
    GroupList,
    HandleAuthorizationView,
    UserList,
)

urlpatterns = [
    path("list/", UserList.as_view()),
    path("groups/", GroupList.as_view()),
    path("authorize/", CustomAuthorizationView.as_view()),
    path(
        "authorize/handle/",
        HandleAuthorizationView.as_view(),
        name="handle_authorization",
    ),
    # path("oauth/authorize/", authorize_request, name="oauth_authorize"),
    # path("oauth/token/", get_access_token, name="oauth_token"),
    # path("oauth/callback/", oauth_callback, name="oauth_callback"),
    # ...
]
