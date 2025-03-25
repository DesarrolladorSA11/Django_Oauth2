from django.urls import path

from .views import (  # get_access_token,
    GroupList,
    UserList,
    authorize_request,
    oauth_callback,
)

urlpatterns = [
    path("list/", UserList.as_view()),
    path("groups/", GroupList.as_view()),
    path("oauth/authorize/", authorize_request, name="oauth_authorize"),
    # path("oauth/token/", get_access_token, name="oauth_token"),
    path("oauth/callback/", oauth_callback, name="oauth_callback"),
    # ...
]
