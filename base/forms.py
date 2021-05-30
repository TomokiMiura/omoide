from django.forms import ModelForm
from . models import OmoideTran


class OmoideCreateForm(ModelForm):
    class Meta:
        model=OmoideTran
        fields=[
            'couple_id',
            'title',
            'posttime',
        ]