from django.urls import path
from .views import PostDetailView, PostListView, CategoryView, TagView, IndexView, CommentView

app_name = 'blogs'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<category_id>/', CategoryView.as_view(), name='category'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='detail'),
    path('comment/', CommentView.as_view(), name='comment'),
]
