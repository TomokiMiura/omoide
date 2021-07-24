from django.forms import ModelForm
from django import forms
from . models import OmoideTran,TextTran,CoupleMaster
import datetime

class OmoideCreateForm(forms.ModelForm):
    class Meta:
        model=OmoideTran
        fields=[
            'couple_id',
            'title',
            'posttime',
            'thumbnail',
        ]
        widgets = {
            'posttime': forms.SelectDateWidget(years=[x for x in range(1990, 2099)])
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['couple_id'].empty_label = '選択してね'

class TextModelForm(forms.ModelForm):
    class Meta:
        model=TextTran
        fields=[
            'text',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    # コメントを保存するメソッド
    def save_comment(self,omoide_id,commit=True):
        # TextTranモデルのインスタンスを生成する
        comment = self.save(commit=False)
        # urls.pyから受け取ったpkを元にomoideを特定する
        comment.omoide_id = OmoideTran.objects.get(id=omoide_id)
        comment.posttime = datetime.datetime.now()
        if commit:
        # メソッドの引数commit=Trueなので、comment.save()が実行される
            comment.save()
        return comment