from django import forms


class PostAdminForm(forms.ModelForm):
    summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'vLargeTextField', 'rows':5}), label='摘要', required=False)