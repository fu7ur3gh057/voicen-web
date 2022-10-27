from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.GetProfileAPIView.as_view(), name="get_profile"),
    path("update/", views.UpdateProfileAPIView.as_view(), name="update_profile"),
    path("api-token/", views.update_api_token, name="update_token")
]
