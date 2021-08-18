from django.shortcuts import redirect
from django.test import TestCase,RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from base.models import CoupleMaster,OmoideTran,TextTran
import accounts.models

from hello_omoide.factory import (
    ParentToChild_TextTranFactory,
    ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,
    ParentToChild_UserFactory
)

from base.views import (
    TopView,OmoideListView,OmoideCreateView,
    OmoideConfirmView,OmoideCommentView
)

from base.forms import (
    OmoideCreateForm,TextModelForm
)

class TopViewTests(TestCase):
    """TopViewのテストクラス"""

    def setUp(self):
        self.req_fac = RequestFactory()

    def test_rendering_template(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        request = self.req_fac.get('/')
        response = TopView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class OmoideListViewTests(TestCase):
    """OmoideListViewのテストクラス"""

    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """テスト用のカップルを準備"""
        self.test_couple = ParentToChild_CoupleMasterFactory(
            men_id = self.test_user_men, girl_id = self.test_user_girl
        )

    def test_request_and_response_for_men_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        """思い出一覧表示画面をリクエスト"""
        request = self.req_fac.get('/home')
        """リクエストユーザーをテスト男性ユーザーに設定"""
        request.user = self.test_user_men
        response = OmoideListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_request_and_response_for_girl_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        """思い出一覧表示画面をリクエスト"""
        request = self.req_fac.get('/home')
        """リクエストユーザーをテスト女性ユーザーに設定"""
        request.user = self.test_user_girl
        response = OmoideListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_request_and_response_for_unknown_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        """思い出一覧表示画面をリクエスト"""
        request = self.req_fac.get('/home')
        """リクエストユーザーを匿名ユーザーに設定"""
        request.user = AnonymousUser()
        response = OmoideListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class OmoideCreateViewTests(TestCase):
    """OmoideCreateViewのテストクラス"""

    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """テスト用のカップルを準備"""
        self.test_couple = ParentToChild_CoupleMasterFactory(
            men_id = self.test_user_men, girl_id = self.test_user_girl
        )
    
    def test_request_and_response_for_men_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        # 思い出作成画面をリクエスト
        request = self.req_fac.get('/create_omoide/')
        # リクエストユーザーをテスト男性ユーザーに設定
        request.user = self.test_user_men
        response = OmoideCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_request_and_response_for_girl_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        # 思い出作成画面をリクエスト
        request = self.req_fac.get('/create_omoide/')
        # リクエストユーザーをテスト男性ユーザーに設定
        request.user = self.test_user_girl
        response = OmoideCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_form_valid_next_equal_confirm(self):
        """思い出作成画面にて確認ボタンを押下した時のテスト"""

        test_omoide = {

            'title': 'テスト',
            'posttime': '2020-08-22',
            'next': 'confirm',

        }

        """思い出作成画面をリクエスト"""
        request = self.req_fac.post('/create_omoide/',test_omoide,follow=True)
        """リクエストユーザーをテスト男性ユーザーに設定"""
        request.user = self.test_user_men
        response = OmoideCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/confirm_omoide/1'
        )

    def test_form_valid_next_equal_back(self):
        """思い出作成画面にて戻るボタンを押下した時のテスト"""

        test_omoide = {

            'title': 'テスト',
            'posttime': '2020-08-22',
            'next': 'back',

        }

        """思い出作成画面をリクエスト"""
        request = self.req_fac.post('/create_omoide/',test_omoide,follow=True)
        """リクエストユーザーをテスト男性ユーザーに設定"""
        request.user = self.test_user_men
        response = OmoideCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_form_valid_next_None(self):
        """思い出作成画面にてnextの値がconfirm,back以外の時のテスト"""

        test_omoide = {

            'title': 'テスト',
            'posttime': '2020-08-22',
            'next': 'hogehoge',

        }

        """思い出作成画面をリクエスト"""
        request = self.req_fac.post('/create_omoide/',test_omoide,follow=True)
        """リクエストユーザーをテスト男性ユーザーに設定"""
        request.user = self.test_user_men
        response = OmoideCreateView.as_view()(request)
        self.assertURLEqual(
            response.url, '/home'
        )

class OmoideConfirmViewTests(TestCase):
    """OmoideConfirmViewのテストクラス"""

    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        # 男性ユーザー、女性ユーザーを準備
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        # テスト用のカップルを準備
        self.test_couple = ParentToChild_CoupleMasterFactory(men_id = self.test_user_men, girl_id = self.test_user_girl)
        # テスト用の思い出を準備
        self.test_omoide1 = ParentToChild_OmoideTranFactory(
            couple_id = self.test_couple,
            title='テスト1',
            thumbnail__color='green',
            thumbnail__height=300,
            thumbnail__width=300,
            thumbnail__filename='test.jpg',
            thumbnail__format='JPEG',
        )

    def test_request_and_response_for_men_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        # テスト用の思い出のPKを保存
        test_omoide_pk = self.test_omoide1.pk
        request = self.req_fac.get('/confirm_omoide/')
        request.user = self.test_user_men
        # リクエストユーザーをテスト男性ユーザーに設定
        response = OmoideConfirmView.as_view()(request,pk=test_omoide_pk)
        self.assertEqual(response.status_code, 200)

    def test_request_and_response_for_girl_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        # テスト用の思い出のPKを保存
        test_omoide_pk = self.test_omoide1.pk
        request = self.req_fac.get('/confirm_omoide/')
        request.user = self.test_user_girl
        # リクエストユーザーをテスト男性ユーザーに設定
        response = OmoideConfirmView.as_view()(request,pk=test_omoide_pk)
        self.assertEqual(response.status_code, 200)

class OmoideCommentViewTests(TestCase):
    """OmoideCommentViewのテストクラス"""
    
    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        # 男性ユーザー、女性ユーザーを準備
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        # テスト用のカップルを準備
        self.test_couple = ParentToChild_CoupleMasterFactory(men_id = self.test_user_men, girl_id = self.test_user_girl)
        # テスト用の思い出を準備
        self.test_omoide1 = ParentToChild_OmoideTranFactory(
            couple_id = self.test_couple,
            title='テスト1',
            thumbnail__color='green',
            thumbnail__height=300,
            thumbnail__width=300,
            thumbnail__filename='test.jpg',
            thumbnail__format='JPEG',
        )

    def test_request_and_response_for_men_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        test_omoide_pk = self.test_omoide1.pk
        request = self.req_fac.get('/post/')
        request.user = self.test_user_men
        # リクエストユーザーをテスト男性ユーザーに設定
        response = OmoideCommentView.as_view()(request,pk=test_omoide_pk)
        self.assertEqual(response.status_code, 200)

    def test_request_and_response_for_girl_user(self):
        """GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        test_omoide_pk = self.test_omoide1.pk
        request = self.req_fac.get('/post/')
        request.user = self.test_user_girl
        # リクエストユーザーをテスト男性ユーザーに設定
        response = OmoideCommentView.as_view()(request,pk=test_omoide_pk)
        self.assertEqual(response.status_code, 200)  
    
    def test_form_saved(self):
        """思い出作成画面にて確認ボタンを押下した時のテスト"""
        test_omoide_pk = self.test_omoide1.pk
        test_text = {

            'text': 'テストです',

        }
        """メッセージ作成し、投稿後の画面をリクエスト"""
        request = self.req_fac.post('/post/',test_text,follow=True)
        """リクエストユーザーをテスト男性ユーザーに設定"""
        request.user = self.test_user_men
        response = OmoideCommentView.as_view()(request,pk=test_omoide_pk)
        self.assertURLEqual(
            response.url, '/post/1'
        )

