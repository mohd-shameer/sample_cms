from django.urls import path
from rest_framework import routers

from cms.apps.article import views

router = routers.SimpleRouter()
router.register("", views.ArticleViewset, basename="article")

app_name='article'
urlpatterns = [
    path("file/<str:id>/", views.ArticleDownload.as_view(), name="article-download"),
    path("search/", views.ArticleQuery.as_view(), name="article-query")
] + router.urls
