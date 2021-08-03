from django.forms import ModelForm,FileInput
from django import forms
from django.db.models import Q
from . models import OmoideTran,TextTran,CoupleMaster
import datetime

class OmoideCreateForm(forms.ModelForm):

    # thumbnail = forms.ImageField(widget=MyImageWidget)

    class Meta:
        model=OmoideTran
        fields=[
            'title',
            'posttime',
            'thumbnail',
        ]
        widgets = {
            'posttime': forms.SelectDateWidget(years=[x for x in range(2000, 2031)],
                        empty_label=("何年？","何月？","何日？")),
        }
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        
    def save(self,user,commit=True,**kwargs):
        # フォームのインスタンスomoideを作成,""
        omoide = super().save(commit=False)
        # CoupleMasterのインスタンスが必要
        couple_instance = CoupleMaster.objects.get(
            Q(men_id=user) | Q(girl_id=user)
        )    
        omoide.couple_id = couple_instance 
        if commit:
            omoide.save()
        return omoide

class TextModelForm(forms.ModelForm):
    class Meta:
        model=TextTran
        fields = [
            'text',
            'image',
        ]
        widgets = {

            'text': forms.TextInput(attrs={'placeholder': 'メッセージを入力してね!'}),

        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    # コメントを保存するメソッド
    def save_comment(self,omoide_id,user,commit=True):
        # TextTranモデルのインスタンスを生成する
        comment = self.save(commit=False)
        # urls.pyから受け取ったpkを元にomoideを特定する
        comment.omoide_id = OmoideTran.objects.get(id=omoide_id)
        comment.author_id = user
        comment.posttime = datetime.datetime.now()
        if commit:
        # メソッドの引数commit=Trueなので、comment.save()が実行される
            comment.save()
        return comment