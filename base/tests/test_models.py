from django.test import TestCase
from base.models import CoupleMaster,OmoideTran,TextTran
from accounts.models import User
import datetime

import tempfile

from hello_omoide.factory import (
    ParentToChild_TextTranFactory,
    ParentToChild_OmoideTranFactory,
    ParentToChild_CoupleMasterFactory,
    ParentToChild_UserFactory
)

from django.utils import timezone
from freezegun import freeze_time

class CoupleMasterModelTests(TestCase):

    def setUp(self):
        """テスト用のモデルを準備する"""
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)

    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_couple = CoupleMaster.objects.all()
        self.assertEqual(saved_couple.count(), 0)
    
    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        test_couple = CoupleMaster(
            men_id=self.test_user_men, girl_id=self.test_user_girl
        )
        test_couple.save()
        saved_couple = CoupleMaster.objects.all()
        self.assertEqual(saved_couple.count(), 1)

    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        CoupleMaster.objects.create(
            men_id=self.test_user_men, girl_id=self.test_user_girl
        )
        saved_couple = CoupleMaster.objects.all()
        actual_couple = saved_couple[0]

        self.assertEqual(actual_couple.men_id, self.test_user_men)
        self.assertEqual(actual_couple.girl_id, self.test_user_girl)

class OmoideTranModelTests(TestCase):

    def setUp(self):
        """テスト用のモデルを準備する"""
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """男性ユーザー、女性ユーザーをカップルに設定"""
        self.test_couple = ParentToChild_CoupleMasterFactory(
            men_id = self.test_user_men, girl_id = self.test_user_girl
        )
        """テスト用の画像(png形式)を準備"""
        self.test_thumbnail = tempfile.NamedTemporaryFile(suffix=".jpg").name

    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_omoide = OmoideTran.objects.all()
        self.assertEqual(saved_omoide.count(), 0)

    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        OmoideTran.objects.create(
            couple_id = self.test_couple,
            title = 'テスト1',
            posttime = datetime.date(2021, 8, 22),
            thumbnail = self.test_thumbnail
        )
        saved_omoide = OmoideTran.objects.all()
        self.assertEqual(saved_omoide.count(), 1)

    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        test_title = 'テスト'
        test_posttime = datetime.date(2020, 8, 22)
        test_omoide = OmoideTran.objects.create(
            couple_id=self.test_couple,
            title=test_title,
            posttime=test_posttime,
            thumbnail=self.test_thumbnail
        )
        saved_omoide = OmoideTran.objects.all()
        actual_omoide = saved_omoide[0]

        self.assertEqual(actual_omoide.couple_id, self.test_couple)
        self.assertEqual(actual_omoide.title, test_title)
        self.assertEqual(actual_omoide.posttime, test_posttime)
        self.assertEqual(actual_omoide.thumbnail, self.test_thumbnail)

    def test_model_instance(self):
        """OmoideTranのコンストラクタを調べる"""
        saved_omoide = OmoideTran.objects.create(
            couple_id = self.test_couple,
            title = 'テスト1',
            posttime = datetime.date(2021, 8, 22),
            thumbnail = self.test_thumbnail
        )
        self.assertEqual(str(saved_omoide), saved_omoide.title)

class TextTranModelTests(TestCase):

    def setUp(self):
        """テスト用のモデルを準備する"""
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """男性ユーザー、女性ユーザーをカップルに設定"""
        self.test_couple = ParentToChild_CoupleMasterFactory(
            men_id = self.test_user_men, girl_id = self.test_user_girl
        )
        """テスト用の画像(png形式)を準備"""
        self.test_thumbnail = tempfile.NamedTemporaryFile(suffix=".jpg").name
        """テスト用の思い出を３つ準備"""
        self.test_omoide1 = ParentToChild_OmoideTranFactory(
            couple_id = self.test_couple, 
            title='テスト1',
            thumbnail = self.test_thumbnail
        )

    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""  
        saved_text = TextTran.objects.all()
        self.assertEqual(saved_text.count(), 0)

    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""

        test_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        test_text = TextTran.objects.create(
            omoide_id=self.test_omoide1,
            author_id=self.test_user_men,
            posttime='2021-08-22 21:12:24.333404+00:00',
            text='テスト',
            image=test_image
        )

        saved_text = TextTran.objects.all()
        self.assertEqual(saved_text.count(), 1)

    @freeze_time('2020-01-01 01:01:01')
    def test_saving_and_retrieving_post(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        test_message='テスト'
        test_posttime = datetime.datetime(2020, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
        test_image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        test_text = TextTran.objects.create(
            omoide_id=self.test_omoide1,
            author_id=self.test_user_men,
            posttime=test_posttime,
            text=test_message,
            image=test_image
        )
        test_text.save()

        saved_text = TextTran.objects.all()
        actual_text = saved_text[0]

        self.assertEqual(actual_text.omoide_id, self.test_omoide1)
        self.assertEqual(actual_text.author_id, self.test_user_men)
        self.assertEqual(actual_text.posttime, datetime.datetime(2020, 1, 1, 1, 1, 1, tzinfo=timezone.utc))
        self.assertEqual(actual_text.text, test_message)
        self.assertEqual(actual_text.image, test_image)

    @freeze_time('2020-01-01 01:01:01')
    def test_model_instance(self):
        """TextTranのコンストラクタを調べる"""
        test_message='テスト'
        test_posttime = datetime.datetime(2020, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
        test_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        
        saved_message = TextTran.objects.create(
            omoide_id = self.test_omoide1,
            author_id=self.test_user_men,
            posttime=test_posttime,
            text=test_message,
            image=test_image
        )
        self.assertEqual(str(saved_message), saved_message.text)