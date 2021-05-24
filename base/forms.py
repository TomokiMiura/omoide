from django import forms

class OmoideCreateForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        max_length=30,
        required=True,
    )

    posttime = forms.DateTimeField(
        label='思い出の日',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d']
    )