from django.test import TestCase,RequestFactory
from django.urls import reverse
from base.models import CoupleMaster,OmoideTran,TextTran
from accounts.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from accounts.views import (
    MenUserCreateView,GirlUserCreateView,
    UserProfileView,
    UserChangeView,CustomLoginView,
    CustomLogoutView,CustomPasswordChangeView,
    CustomPasswordChangeDoneView,CustomPasswordResetView,
    CustomPasswordResetDoneView,CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView

)

from hello_omoide.factory import (
    ParentToChild_TextTranFactory,
    ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,
    ParentToChild_UserFactory
)

from base.views import (
    OmoideListView,OmoideCreateView,
    OmoideConfirmView,OmoideCommentView
)

from accounts.forms import (
    UserInfoChangeForm,CustomAuthenticationForm,
    CustomPasswordChangeForm,CustomPasswordResetForm,
    CustomSetPasswordForm,AdminUserCreationForm,
    CustomUserChangeForm,CustomUserCreationForm
)

import datetime

import os

class UserInfoChangeFormTests(TestCase):
    """UserInfoChangeFormのテスト"""
    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        """テスト用の男性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
    
    def test_form_init(self):
        """UserInfoChangeFormのコンストラクタのテスト"""
        request = self.req_fac.get('/accounts/change')
        request.user = self.test_user_men
        response = UserChangeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_form_update_method(self):
        """UserInfoChangeFormのupdateメソッドのテスト"""
        test_user_info = {

            'email': 'test1@test.com',
            'username': 'テスト',

        }
        request = self.req_fac.post('/accounts/change',test_user_info)
        request.user = self.test_user_men
        response = UserChangeView.as_view()(request)
        self.assertURLEqual(
            response.url, '/accounts/profile/'
        )

class CustomPasswordChangeFormTests(TestCase):
    """CustomPasswordChangeFormのテスト"""
    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        """テスト用の男性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
    
    def test_form_init(self):
        """CustomPasswordChangeFormのコンストラクタのテスト"""
        request = self.req_fac.get('/accounts/password_change')
        request.user = self.test_user_men
        response = CustomPasswordChangeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

class CustomSetPasswordFormTests(TestCase):
    """CustomSetPasswordFormのテスト"""
    def setUp(self):
        """テストユーザーを1名登録"""
        self.test_user_men = User.objects.create(
            username='テスト', 
            email='test@test.com', 
            password='123'
        )
    
    def test_form_init(self):
        """CustomSetPasswordFormのコンストラクタのテスト"""
        update_password={
                'new_password1': 'hellonewpassword',
                'new_password2': 'hellonewpassword',
        }
        form = CustomSetPasswordForm(self.test_user_men,update_password)
        self.assertTrue(form.is_valid())


        