from django.test import TestCase,RequestFactory,Client
from django.urls import reverse
from base.models import CoupleMaster,OmoideTran,TextTran
import accounts.models

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

from base.forms import (
    OmoideCreateForm,TextModelForm
)

from PIL import Image, ImageFilter
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

import datetime

class OmoideCreateFormTests(TestCase):
    """OmoideCreateFormのテスト"""

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
        """テスト用の画像(png形式)を準備"""
        img_file = BytesIO()
        img = Image.new('RGBA', size=(300,300), color=(255, 255, 255))
        img.save(img_file, 'png')
        img_file.name = 'test_img.png'
        img_file.seek(0)
        self.img_dict = {
            'thumbnail': SimpleUploadedFile(
                    img_file.name,
                    img_file.read(),
                    content_type='image/png'
                    )
        }

    def test_form_validation(self):
        """OmoideCreateFormのバリデーションのテスト"""

        test_input = {

            'title': 'テスト1',
            'posttime': '2020-08-22',

        }

        form = OmoideCreateForm(test_input,self.img_dict)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        """OmoideCreateFormで保存したデータが保存されているか"""

        test_input = {

            'title': 'テスト1',
            'posttime': '2020-08-22',

        }

        form = OmoideCreateForm(test_input,self.img_dict)
        form.save(user=self.test_user_men)
        saved_omoide = OmoideTran.objects.filter(couple_id=self.test_couple)
        self.assertEqual(saved_omoide[0].title, 'テスト1')
        self.assertEqual(saved_omoide[0].posttime, datetime.date(2020, 8, 22))
        self.assertTrue(saved_omoide[0].thumbnail)

class TextModelFormTests(TestCase):
    """TextModelFormのテスト"""
    
    def setUp(self):
        """テスト用のモデルを準備する"""
        self.req_fac = RequestFactory()
        """男性ユーザー、女性ユーザーを準備"""
        self.test_user_men = ParentToChild_UserFactory(is_men = True)
        self.test_user_girl = ParentToChild_UserFactory(is_girl = True)
        """テスト用のカップルを準備"""
        self.test_couple = ParentToChild_CoupleMasterFactory(men_id = self.test_user_men, girl_id = self.test_user_girl)
        """テスト用の思い出を準備"""
        self.test_omoide1 = ParentToChild_OmoideTranFactory(couple_id = self.test_couple, title='テスト1')
        """テスト用の画像(png形式)を準備"""
        img_file = BytesIO()
        img = Image.new('RGBA', size=(300,300), color=(255, 255, 255))
        img.save(img_file, 'png')
        img_file.name = 'test_img.png'
        img_file.seek(0)
        self.img_dict = {
            'image': SimpleUploadedFile(
                    img_file.name,
                    img_file.read(),
                    content_type='image/png'
                    )
        }

    def test_form_validation(self):
        """TextModelFormのバリデーションのテスト"""

        test_input = {

            'text': 'テストです',

        }

        form = TextModelForm(test_input,self.img_dict)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        """OmoideCreateFormで保存したデータが保存されているか"""

        test_input = {

            'text': 'テストです',

        }

        form = TextModelForm(test_input,self.img_dict)
        form.save_comment(
            omoide_id = self.test_omoide1.pk,user=self.test_user_men
        )
        saved_message = TextTran.objects.filter(omoide_id=self.test_omoide1)
        self.assertEqual(saved_message[0].text, 'テストです')
        self.assertTrue(saved_message[0].image)