from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (
    TopView,OmoideListView,OmoideCommentView,
    OmoideCreateView,OmoideConfirmView
)
class TestUrls(TestCase):

    """indexページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_top_url(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, TopView)

    """投稿一覧ページへのリダイレクトをテスト"""
    def test_post_list_url(self):
        view = resolve('/home')
        self.assertEqual(view.func.view_class, OmoideListView)

    """投稿詳細ページへのリダイレクトをテスト"""
    def test_post_commnet_url(self):
        view = resolve('/post/1')
        self.assertEqual(view.func.view_class, OmoideCommentView)

    """投稿作成ページへのリダイレクトをテスト"""
    def test_post_create_url(self):
        view = resolve('/create_omoide/')
        self.assertEqual(view.func.view_class, OmoideCreateView)

    """投稿内容確認ページへのリダイレクトをテスト"""
    def test_post_confirm_url(self):
        view = resolve('/confirm_omoide/1')
        self.assertEqual(view.func.view_class, OmoideConfirmView)