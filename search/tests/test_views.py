from django.test import TestCase,RequestFactory,Client
from django.urls import reverse
from base.models import CoupleMaster,OmoideTran,TextTran
import accounts.models
from hello_omoide.factory import (
    ParentToChild_TextTranFactory,ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,ParentToChild_UserFactory
)

from search.views import SearchResultView

class SearchResultViewTests(TestCase):
    """SearchResultViewのテストクラス"""

    def setUp(self):
        self.req_fac = RequestFactory()
        # テスト用の男性ユーザー、女性ユーザーを準備
        self.test_user_men = ParentToChild_UserFactory(is_men = True,is_girl = False)
        self.test_user_girl = ParentToChild_UserFactory(is_men = False,is_girl = True)
        # テスト用のカップルを準備
        self.test_couple = ParentToChild_CoupleMasterFactory(men_id = self.test_user_men, girl_id = self.test_user_girl)
        # テスト用の思い出を1つ準備
        self.test_omoide1 = ParentToChild_OmoideTranFactory(couple_id = self.test_couple, title='テスト1')
    
    def test_rendering_template(self):
        """テスト用の男性ユーザーでログイン"""
        """テスト用の思い出のタイトルで検索した時のレスポンスのテスト"""
        request = self.req_fac.get('/search/', {'q': 'テスト1'})
        request.user = self.test_user_men
        response = SearchResultView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_rendering_none_template(self):
        """テスト用の男性ユーザーでログイン"""
        """テスト用の思い出のタイトルで未入力で検索した時のレスポンスのテスト"""
        request = self.req_fac.get('/search/', {'q': ''})
        request.user = self.test_user_men
        response = SearchResultView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_rendering_template_for_girl_user(self):
        """テスト用の女性ユーザーでログイン"""
        """テスト用の思い出のタイトルで検索した時のレスポンスのテスト"""
        request = self.req_fac.get('/search/', {'q': 'テスト1'})
        request.user = self.test_user_girl
        response = SearchResultView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_rendering_none_template_for_girl_user(self):
        """テスト用の女性ユーザーでログイン"""
        """テスト用の思い出のタイトルで未入力で検索した時のレスポンスのテスト"""
        request = self.req_fac.get('/search/', {'q': ''})
        request.user = self.test_user_girl
        response = SearchResultView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        

