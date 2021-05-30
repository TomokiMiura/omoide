from django import forms
from . models import OmoideTran,CoupleMaster

class OmoideCreateForm(forms.ModelForm):
    class Meta:
        model=OmoideTran
        fields=[
            'couple_id',
            'title',
            'posttime',
        ]

    def __init__(self, *args, **kwargs):
        # kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['couple_id'].empty_label = '選択して下さい'
        self.fields['title'].widget.attrs['value'] = 'タイトルを記入して下さい'
        #self.fields['posttime'].widget.attrs['value'] = '日付を記入して下さい'
        # self.fields['title'].widget.attrs['class'] = 'huga'

class OmoideForm(forms.Form):
    label_suffix = ''
    title = forms.CharField(
        label='タイトル',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'value': 'タイトルを記入してください'}),
    )
    couple_id = forms.ModelChoiceField(
        label='カップルID',
        queryset=CoupleMaster.objects.all(),
        required=True,
        empty_label = '選択して下さい',
    )
    posttime = forms.DateField(
        label='日付',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)    
