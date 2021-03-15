from rest_framework import serializers
from rest_framework.fields import ListField

from cms.apps.article import models


class StringArrayField(ListField):

    def to_internal_value(self, data):
        data = [value.strip() for value in data[0].split(",")]
        return super().to_internal_value(data)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='article:article-detail', lookup_field='id')
    file_download = serializers.HyperlinkedIdentityField(view_name='article:article-download', lookup_field='id')
    categories = StringArrayField()

    def save(self, **kwargs):
        user = self.context['request'].user
        self.validated_data['user'] = user
        return super().save(**kwargs)

    class Meta:
        model = models.Article
        exclude = ['user']
