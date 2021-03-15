from unittest import mock

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from cms.test_utils import api_test_request

from . import views
from cms.apps.authentication.models import CustomUser
from cms.apps.article.models import Article
from cms.apps.authentication.manager import CustomUserManager


class Login(TestCase):

    def setUp(self):
        self.super_usr = CustomUser.objects.create_superuser(**{
            "email": "dummy_mail",
            "password": "dummy_pwd",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        })



    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_invalid_creds(self):
        response = api_test_request(method="post", view=views.Login,
                                    data={"email": "dummy_mail", "password": "dummy_pwd2"})

        self.assertEqual(response.status_code, 401)

    @mock.patch("cms.apps.authentication.views.login")
    def test_login_sanity(self, mock_login):
        mock_login.return_value = True
        response = api_test_request(method="post", view=views.Login,
                                    data={"email": "dummy_mail", "password": "dummy_pwd"})

        self.assertEqual(response.status_code, 200)


class UserViewSetTests(TestCase):

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

    def tearDown(self):
        CustomUser.objects.all().delete()

    def test_getlist_sanity(self):
        response = api_test_request(method={"get": "list"}, view=views.UserViewset, user=self.usr)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        response = api_test_request(method={"get": "list"}, view=views.UserViewset, user=self.super_usr)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_getdetail_sanity(self):
        response = api_test_request(method={"get": "retrieve"}, view=views.UserViewset, user=self.usr, pk=self.usr.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'dummy_mail')

        # Check if the super user is able to read some other user's record
        response = api_test_request(method={"get": "retrieve"}, view=views.UserViewset, user=self.super_usr, pk=self.super_usr.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], 'dummy_smail')

    def test_update_sanity(self):
        response = api_test_request(method={"put": "update"}, view=views.UserViewset,
                                    user=self.usr,
                                    data={
                                        "email": "dummy@gmail.com",
                                        "password": "dummy_pwdB",
                                        "first_name": "abcde",
                                        "last_name": "bcd",
                                        "phone": 1234567891,
                                        "pincode": 123456
                                    }, pk=self.usr.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], "dummy@gmail.com")

    def test_create_sanity(self):
        response = api_test_request(method={"post": "create"}, view=views.UserViewset,
                                    user=self.super_usr,
                                    data={
                                        "email": "super_dummy@gmail.com",
                                        "password": "dummy_pwd",
                                        "first_name": "abcde",
                                        "last_name": "bcd",
                                        "phone": 1234567891,
                                        "pincode": 123456
                                    })

        self.assertEqual(response.status_code, 400)

        response = api_test_request(method={"post": "create"}, view=views.UserViewset,
                                    user=self.super_usr,
                                    data={
                                        "email": "super_dummy@gmail.com",
                                        "password": "dummy_pwdA",
                                        "first_name": "abcde",
                                        "last_name": "bcd",
                                        "phone": 1234567891,
                                        "pincode": 123456
                                    })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], "super_dummy@gmail.com")

    def test_delete_sanity(self):
        response = api_test_request(method={"delete": "destroy"}, view=views.UserViewset,
                                    user=self.usr, pk=self.usr.pk)

        self.assertEqual(response.status_code, 204)

    def test_create_manager_sanity(self):
        obj = {
            "email": "super_dummy@gmail.com",
            "password": "dummy_pwdA",
            "first_name": "abc",
            "last_name": "bcd",
            "phone": 1234567891,
            "pincode": 123456
        }
        user = None
        for key in ["first_name", "last_name", "email"]:
            tmp_obj = obj.copy()
            tmp_obj[key] = None
            try:
                user = CustomUser.objects.create_user(**tmp_obj)
            except ValueError:
                pass
            self.assertIsNone(user)
