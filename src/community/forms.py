from django.forms import ModelForm, Textarea, CharField
from .models import Topic, Reply
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title','channel','topic_body']
        widgets = {
            'topic_body':SummernoteWidget(),
        }
