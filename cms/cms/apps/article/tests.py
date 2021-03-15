from unittest import mock

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from cms.test_utils import api_test_request

from . import views
from cms.apps.authentication.models import CustomUser
from cms.apps.article.models import Article


class ArticleDownloadTests(TestCase):

    def setUp(self):
        self.usr = CustomUser.objects.create(**{
            "email": "dummy_mail",
            "password": "dummy_pwdA",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })

        Article.objects.create(**{
            "id": 1,
            "user": self.usr,
            "title": "sample title",
            "body": "full body text",
            "summary": "aaaaaaaaaaaaaaaaaa",
            "file": SimpleUploadedFile("hr.pdf", b'binary data')
        })

    def tearDown(self):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_download_sanity(self):
        response = api_test_request(view=views.ArticleDownload, user=self.usr, format='multipart', id='1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'binary data')

        response = api_test_request(view=views.ArticleDownload, user=self.usr, format='multipart', id='2')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')


class ArticleViewSetTests(TestCase):

    def setUp(self):
        self.usr = CustomUser.objects.create(**{
            "email": "dummy_mail",
            "password": "dummy_pwdA",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })
        self.super_usr = CustomUser.objects.create_superuser(**{
            "email": "dummy_smail",
            "password": "dummy_spwdA",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })

        Article.objects.create(**{
            "id": 1,
            "user": self.usr,
            "title": "sample title",
            "body": "full body text",
            "summary": "aaaaaaaaaaaaaaaaaa",
            "file": SimpleUploadedFile("hr.pdf", b'binary data')
        })
        Article.objects.create(**{
            "id": 2,
            "user": self.super_usr,
            "title": "sample title2",
            "body": "full body text2",
            "summary": "bbbbbbbbbbbbbbbbbbbb",
            "file": SimpleUploadedFile("hr2.pdf", b'binary data')
        })

    def tearDown(self):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_getlist_sanity(self):
        response = api_test_request(method={"get": "list"}, view=views.ArticleViewset, user=self.usr)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Check if the super user is shown all the articles and not just the one's he created
        response = api_test_request(method={"get": "list"}, view=views.ArticleViewset, user=self.super_usr)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_getdetail_sanity(self):
        response = api_test_request(method={"get": "retrieve"}, view=views.ArticleViewset, user=self.usr, id='1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'sample title')

        # Check if the super user is able to read some other user's article
        response = api_test_request(method={"get": "retrieve"}, view=views.ArticleViewset, user=self.super_usr, id='1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'sample title')

    def test_update_sanity(self):
        response = api_test_request(method={"put": "update"}, view=views.ArticleViewset,
                                    user=self.usr,
                                    data={
                                        "title": "sample user title2",
                                        "body": "sample user body2",
                                        "summary": "sample summary2",
                                        "file": SimpleUploadedFile("hr2.pdf", b'binary data', content_type='application/pdf'),
                                        "categories": ""
                                    }, id='1', format="multipart")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "sample user title2")

    def test_delete_sanity(self):
        response = api_test_request(method={"delete": "destroy"}, view=views.ArticleViewset,
                                    user=self.usr, id='1')

        self.assertEqual(response.status_code, 204)


class ArticleQueryTest(TestCase):
    def setUp(self):
        self.usr = CustomUser.objects.create(**{
            "email": "dummy_mail",
            "password": "dummy_pwd",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })
        self.super_usr = CustomUser.objects.create_superuser(**{
            "email": "dummy_smail",
            "password": "dummy_spwd",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })

        Article.objects.create(**{
            "id": 1,
            "user": self.usr,
            "title": "Understanding Inheritance in JavaScript",
            "body": "A brief overview designed to help you understand the fundamental concepts of inheritance.",
            "summary": "In simple terms, prototypal inheritance refers to objects inheriting properties and methods from "
                       "other objects. These object that properties are being inherited from are called prototypes. "
                       "JavaScript is a prototype based language. It is not class based.",
            "file": SimpleUploadedFile("hr.pdf", b'binary data'),
            "categories": ["sample_category", "sample_category2"],
        })
        Article.objects.create(**{
            "id": 2,
            "user": self.super_usr,
            "title": "How performant are Array methods and Object methods in JavaScript",
            "body": "Analysing the Big O of various Array and Object methods",
            "summary": "Understanding how objects and arrays work through the lens of Big O is an important thing to know, "
                       "as it should influence the choices you make when structuring data in your apps.",
            "file": SimpleUploadedFile("hr2.pdf", b'binary data'),
            "categories": ["sample_category2"],
        })

    def tearDown(self):
        CustomUser.objects.all().delete()
        Article.objects.all().delete()

    def test_query_categories(self):
        response = api_test_request(view=views.ArticleQuery, user=self.usr,
                                    query_string="?categories=sample_category2")

        self.assertEqual(response.status_code, 200)
        # Check if the response doesn't have the article created by superuser as the query is being made by normal user
        self.assertEqual(len(response.data), 1)

    def test_query_title(self):
        response = api_test_request(view=views.ArticleQuery, user=self.super_usr,
                                    query_string="?title=javascript")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Understanding Inheritance in JavaScript")
