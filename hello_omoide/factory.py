# factory_boyをインポート
from factory.django import DjangoModelFactory
# モデルのインポート
from base.models import CoupleMaster,OmoideTran,TextTran
from accounts.models import User
import factory

from factory.fuzzy import FuzzyText,FuzzyDate
from factory import SubFactory

# import os
# from hello_omoide import settings

# テスト用の画像を開くためのモジュールをインポート
import tempfile

import datetime

class ParentToChild_UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = FuzzyText(length=5)
    email = FuzzyText(length=12,suffix='@example.com')
    # デフォルトでis_men,is_girlは0
    # テストコードで適宜変更
    is_men = False
    is_girl = False

class ParentToChild_CoupleMasterFactory(DjangoModelFactory):
    class Meta:
        model = CoupleMaster
        
    men_id = SubFactory(ParentToChild_UserFactory)
    girl_id = SubFactory(ParentToChild_UserFactory)


class ParentToChild_OmoideTranFactory(DjangoModelFactory):

    class Meta:
        model = OmoideTran

    couple_id = SubFactory(ParentToChild_CoupleMasterFactory)
    title = FuzzyText(length=10)
    # 2010年1月1日から現在までの年月日をランダム作成・格納
    posttime = datetime.date(2020, 8, 22)
    thumbnail = factory.django.ImageField()
    

class ParentToChild_TextTranFactory(DjangoModelFactory):
    class Meta:
        model = TextTran
    omoide_id = SubFactory(ParentToChild_OmoideTranFactory)
    posttime = datetime.datetime.now()
    text = FuzzyText(length=20)
    image = factory.django.ImageField()
    