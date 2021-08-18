from django.test import TestCase
from django.core import mail
from base.models import CoupleMaster,OmoideTran,TextTran
from accounts.models import User

from hello_omoide.factory import (
    ParentToChild_TextTranFactory,
    ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,
    ParentToChild_UserFactory
)

class UserModelTests(TestCase):
    
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 0)
    
    def test_is_count_one(self):
        """男性、女性テストユーザーを作成すると、レコードが2つだけカウントされることをテスト"""
        test_men = User.objects.create_men_user(username='テスト', email='test_men@test.com',is_men=True,is_girl=False)
        test_girl = User.objects.create_girl_user(username='テスコ', email='test_girl@test.com',is_men=False,is_girl=True)
        saved_user = User.objects.all()
        self.assertEqual(saved_user.count(), 2)

    def test_create_super_user(self):
        """スーパーユーザーを作成する"""
        test_create_super_user = User.objects.create_superuser(
            email = 'test_super@test.com',
            password = '123',
            is_staff = True,
            is_superuser = True
        )
        saved_super_user = User.objects.filter(is_superuser = True)
        self.assertEqual(saved_super_user.count(), 1)
    
    def test_raise_ValueError_without_email(self):
        """Valueerrorのテスト"""
        with self.assertRaises(ValueError):
            User.objects._create_user(email=None, password='123')

    def test_raise_ValueError_without_is_staff(self):
        """create_superuserメソッドにおけるValueerrorのテスト"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = 'test_super@test.com',
                password = '123',
                is_staff = False,
                is_superuser = False
            )
    
    def test_raise_ValueError_without_is_superuser(self):
        """create_superuserメソッドにおけるValueerrorのテスト"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email = 'test_super@test.com',
                password = '123',
                is_superuser = False
            )

    def test_clear_method(self):
        """clearメソッドのテスト"""
        test_user = User.objects.create(
                username = 'テスト',
                email = 'test１@test.com',
                password = '123',
        )
        test_user.clean()
        self.assertEqual(test_user.email, 'test1@test.com')

    def test_email_user_method(self):
        """email_userメソッドのテスト"""
        test_user = User.objects.create(
                username = 'テスト',
                email = 'test１@test.com',
                password = '123'
        )

        test_user.email_user(
            subject = 'テストの件名',
            message = 'テストのメッセージ',
            from_email = None,
            fail_silently = False
        )

        self.assertEquals(mail.outbox[0].subject, 'テストの件名')
        self.assertEquals(mail.outbox[0].body, 'テストのメッセージ')

    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        test_user = User.objects.create(username='テスト', email='test_men@test.com',is_men=True,is_girl=False)

        saved_user = User.objects.all()
        actual_user = saved_user[0]

        self.assertEqual(actual_user.username, test_user.username)
        self.assertEqual(actual_user.email, test_user.email)
        self.assertEqual(actual_user.is_men, test_user.is_men)
        self.assertEqual(actual_user.is_girl, test_user.is_girl)