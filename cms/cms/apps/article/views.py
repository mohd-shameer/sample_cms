import logging
from wsgiref.util import FileWrapper

from urllib.parse import urlparse, parse_qs
from django.http import HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from cms.apps.article.models import Article
from .serializers import ArticleSerializer

LOGGER = logging.getLogger("cms")


class ArticleViewset(ModelViewSet):
    model = Article
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = self.model.objects.all()
            return queryset.filter(user=self.request.user)
        return super().get_queryset()


class ArticleDownload(APIView):

    def get(self, request, *args, **kwargs):
        obj_id = kwargs.get('id')
        try:
            article_obj = Article.objects.get(id=obj_id)
        except Article.DoesNotExist:
            LOGGER.error(f"Article object with id {obj_id} not found.")
            raise exceptions.NotFound()

        wrapper = FileWrapper(article_obj.file.file.open(mode="rb"))

        response = HttpResponse(wrapper, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename:{article_obj.file.name}"
        response["Content-Length"] = article_obj.file.size
        return response


class ArticleQuery(APIView):

    def get(self, request, *args, **kwargs):
        query = request.query_params
        field_names = [field.name for field in Article._meta.fields]

        query_key = list(query.keys())[0]
        if not query_key in field_names:
            raise exceptions.ParseError(f"Please check the query parameter. Searching on field {query_key} is not possible.")

        if request.user.is_superuser:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(user=request.user)

        if query_key == 'categories':
            articles = queryset.filter(categories__icontains=query[query_key])
        else:
            articles = queryset.annotate(rank=SearchRank(SearchVector(query_key),
                                                         SearchQuery(query[query_key]))).order_by('-rank')

        return Response([{
            "title": article.title,
            "body": article.body,
            "summary": article.summary,
            "categories": article.categories,
            "file_download": reverse("article:article-download", kwargs={'id': article.id}),
            "url": reverse("article:article-detail", kwargs={'id': article.id}),
        } for article in articles])
