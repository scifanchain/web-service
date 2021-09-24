from django.forms import ModelForm
from works.models import Stage


class StageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['title', 'content']
