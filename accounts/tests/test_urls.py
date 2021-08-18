from django.test import TestCase
from django.urls import reverse, resolve
from ..views import (

    MenUserCreateView,GirlUserCreateView,CustomLoginView,
    CustomLogoutView,CustomPasswordChangeView,CustomPasswordChangeDoneView,
    CustomPasswordResetView,CustomPasswordResetDoneView,CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,UserChangeView,UserProfileView

)

class TestUrls(TestCase):

    """男性ユーザー向けのサインアップページへアクセスする時のリダイレクトをテスト"""
    def test_signup_men_url(self):
        view = resolve('/accounts/signup_men/')
        self.assertEqual(view.func.view_class, MenUserCreateView)

    """女性ユーザー向けのサインアップページへアクセスする時のリダイレクトをテスト"""
    def test_signup_girl_url(self):
        view = resolve('/accounts/signup_girl/')
        self.assertEqual(view.func.view_class, GirlUserCreateView)

    """ログインページへアクセスする時のリダイレクトをテスト"""
    def test_login_url(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.view_class, CustomLoginView)

    """ログアウトページへアクセスする時のリダイレクトをテスト"""
    def test_logout_url(self):
        view = resolve('/accounts/logout/')
        self.assertEqual(view.func.view_class, CustomLogoutView)

    """パスワード変更ページへアクセスする時のリダイレクトをテスト"""
    def test_password_change_url(self):
        view = resolve('/accounts/password_change/')
        self.assertEqual(view.func.view_class, CustomPasswordChangeView)

    """パスワード変更完了ページへアクセスする時のリダイレクトをテスト"""
    def test_password_change_done_url(self):
        view = resolve('/accounts/password_change/done/')
        self.assertEqual(view.func.view_class, CustomPasswordChangeDoneView)

    """パスワードリセットページへアクセスする時のリダイレクトをテスト"""
    def test_password_reset_url(self):
        view = resolve('/accounts/password_reset/')
        self.assertEqual(view.func.view_class, CustomPasswordResetView)

    """パスワードリセットメール送信完了ページへアクセスする時のリダイレクトをテスト"""
    def test_password_reset_done_url(self):
        view = resolve('/accounts/password_reset/done/')
        self.assertEqual(view.func.view_class, CustomPasswordResetDoneView)

    """パスワードリセット確認ページへアクセスする時のリダイレクトをテスト"""
    def test_password_reset_confirm_done_url(self):
        view = resolve('/accounts/reset/<uidb64>/<token>/')
        self.assertEqual(view.func.view_class, CustomPasswordResetConfirmView)

    """パスワードリセット完了ページへアクセスする時のリダイレクトをテスト"""
    def test_password_reset_complete_url(self):
        view = resolve('/accounts/reset/done/')
        self.assertEqual(view.func.view_class, CustomPasswordResetCompleteView)

    """ユーザー情報変更ページへアクセスする時のリダイレクトをテスト"""
    def test_user_profile_change_url(self):
        view = resolve('/accounts/change/')
        self.assertEqual(view.func.view_class, UserChangeView)

    """ユーザー情報確認ページへアクセスする時のリダイレクトをテスト"""
    def test_user_profile_url(self):
        view = resolve('/accounts/profile/')
        self.assertEqual(view.func.view_class, UserProfileView)