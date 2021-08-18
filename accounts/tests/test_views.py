from django.test import TestCase,RequestFactory,Client
from django.core import mail
from django.urls import reverse
from base.models import CoupleMaster,OmoideTran,TextTran
from accounts.models import User

from hello_omoide.factory import (
    ParentToChild_TextTranFactory,ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,ParentToChild_UserFactory
)

from accounts.views import (

    MenUserCreateView,GirlUserCreateView,CustomLoginView,
    CustomLogoutView,CustomPasswordChangeView,CustomPasswordChangeDoneView,
    CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,UserChangeView,UserProfileView

)

from base.models import ( 

    CoupleMaster,OmoideTran,TextTran

)

class MenUserCreateViewTests(TestCase):
    """MenUserCreateViewのテストクラス"""
    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:create_men_user'))
        self.assertEqual(response.status_code, 200)

    def test_create_men_user_confirm(self):
        """確認ボタン押下した時のテスト"""

        test_men_user = {

            'username': 'テストメンズ',
            'email': 'test_men@test.com',
            'is_men': True,
            'is_girl': False,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'confirm',

        }
        """男性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_men/',test_men_user,follow=True)
        response = MenUserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_men_user_back(self):
        """戻るボタンを押下した時のテスト"""

        test_men_user = {

            'username': 'テストメンズ',
            'email': 'test_men@test.com',
            'is_men': True,
            'is_girl': False,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'back',

        }
        """男性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_men/',test_men_user,follow=True)
        response = MenUserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_men_user_regist(self):
        """登録ボタンを押下した時のテスト"""

        test_men_user = {

            'username': 'テストメンズ',
            'email': 'test_men@test.com',
            'is_men': True,
            'is_girl': False,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'regist',

        }
        """男性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_men/',test_men_user,follow=True)
        response = MenUserCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/accounts/signup_girl/'
        )
    
    def test_create_men_user_else(self):
        """例外が発生した時のテスト"""

        test_men_user = {

            'username': 'テストメンズ',
            'email': 'test_men@test.com',
            'is_men': True,
            'is_girl': False,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'hogehoge',

        }
        """男性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_men/',test_men_user,follow=True)
        response = MenUserCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/'
        )

class GirlUserCreateViewTests(TestCase):
    """GirlUserCreateViewのテストクラス"""

    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_couple = ParentToChild_CoupleMasterFactory(men_id = self.test_user_men)

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:create_girl_user'))
        self.assertEqual(response.status_code, 200)

    def test_create_girl_user_confirm(self):
        """確認ボタン押下した時のテスト"""

        test_girl_user = {

            'username': 'テストガール',
            'email': 'test_girl@test.com',
            'is_men': False,
            'is_girl': True,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'confirm',

        }
        """女性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_girl/',test_girl_user,follow=True)
        response = GirlUserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_gril_user_back(self):
        """戻るボタンを押下した時のテスト"""

        test_girl_user = {

            'username': 'テストガール',
            'email': 'test_girl@test.com',
            'is_men': False,
            'is_girl': True,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'back',

        }
        """女性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_girl/',test_girl_user,follow=True)
        response = GirlUserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_create_girl_user_regist(self):
        """登録ボタンを押下した時のテスト"""

        test_girl_user = {

            'username': 'テストガールズ',
            'email': 'test_girl@test.com',
            'is_men': False,
            'is_girl': True,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'regist',

        }

        """女性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_girl/',test_girl_user,follow=True)
        request.COOKIES = { 
            'men_data': self.test_user_men
        }
        response = GirlUserCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/accounts/login/'
        )
    
    def test_create_men_user_else(self):
        """例外が発生した時のテスト"""

        test_girl_user = {

            'username': 'テストメンズ',
            'email': 'test_men@test.com',
            'is_men': True,
            'is_girl': False,
            'password1': 'helloomoide',
            'password2': 'helloomoide',
            'next': 'hogehoge',

        }
        """女性用サインアップ画面をリクエスト"""
        request = self.req_fac.post('/accounts/signup_girl/',test_girl_user,follow=True)
        response = GirlUserCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/'
        )

class CustomLoginViewTests(TestCase):
    """CustomLoginViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

class CustomLogoutViewTests(TestCase):
    """CustomLogoutViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:logout'))
        # ログアウト機能としてログインページにリダイレクトされるため302
        self.assertEqual(response.status_code, 302)

class CustomPasswordChangeViewTests(TestCase):
    """CustomPasswordChangeViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:password_change'))
        # パスワード変更完了画面にリダイレクトされるため302
        self.assertEqual(response.status_code, 302)

class CustomPasswordChangeDoneViewTests(TestCase):
    """CustomPasswordChangeDoneViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:password_change_done'))
        self.assertEqual(response.status_code, 302)

class CustomPasswordResetViewTests(TestCase):
    """CustomPasswordResetViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)

class CustomPasswordResetDoneViewTests(TestCase):
    """CustomPasswordResetDoneViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:password_reset_done'))
        self.assertEqual(response.status_code, 200)

class CustomPasswordResetConfirmViewTests(TestCase):
    """CustomPasswordResetConfirmViewのテストクラス"""

    def setUp(self):
        """テストユーザーを1名登録"""
        User.objects.create(username='テスト', email='test@test.com', password='123')
        self.response = self.client.post(reverse('accounts:password_reset'), { 'email': 'test@test.com' })
        self.email = mail.outbox[0]

    def test_email_subject(self):
        """パスワードリセットメールの件名のテスト"""
        self.assertEqual('パスワード再設定を受け付けました', self.email.subject)

    def test_email_body(self):
        """パスワードリセットメールの内容のテスト"""
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('テスト', self.email.body)

    def test_email_to(self):
        """パスワードリセットメールの送信先のテスト"""
        self.assertEqual(['test@test.com',], self.email.to)

    def test_email_from(self):
        """パスワードリセットメールの送信元のテスト"""
        self.assertEqual('omoide.contact.official@gmail.com', self.email.from_email)

class CustomPasswordResetCompleteViewTests(TestCase):
    """CustomPasswordResetCompleteViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('accounts:password_reset_complete'))
        self.assertEqual(response.status_code, 200)

class UserChangeViewTests(TestCase):
    """UserChangeViewのテストクラス"""

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード302を返されることを確認"""
        response = self.client.get(reverse('accounts:change'))
        self.assertEqual(response.status_code, 302)

class UserProfileViewTests(TestCase):
    """UserProfileViewのテストクラス"""

    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """テスト用のカップルを準備"""
        self.test_couple = ParentToChild_CoupleMasterFactory(
            men_id = self.test_user_men, girl_id = self.test_user_girl
        )

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        request = self.req_fac.get('/accounts/profile/')
        request.user = self.test_user_men
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)