from rest_framework import routers

from django.urls import path

from .views import Login, UserViewset

router = routers.SimpleRouter()
router.register("account", UserViewset, basename="account")

urlpatterns = [
    path("login/", Login.as_view(), name="api-login")
] + router.urls
