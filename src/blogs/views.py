from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Comment, Post, Status
from .forms import CommentForm
import markdown
from django.views.generic import DetailView, ListView, TemplateView
from django.core.paginator import Paginator


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = (Category.get_menus())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.objects.filter(status=Status.STATUS_NORMAL) \
        .select_related('owner') \
        .select_related('category')
    paginate_by = 19
    context_object_name = 'posts'
    template_name = 'blogs/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context["category"] = category
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tags__id=tag_id)


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 10
    context_object_name = 'posts'
    template_name = 'blogs/list.html'


class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    queryset = Post.latest_posts()
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'blogs/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        context["comment_form"] = CommentForm
        context['comment_list'] = Comment.get_by_post(post_id)
        return context

    def get_object(self):
        post = super().get_object()
        post.content = markdown.markdown(post.content, extensions=[
            'markdown.extensions.extra',  # 标题、表格、引用等基本转换
            'markdown.extensions.codehilite',  # 语法高亮拓展
            'markdown.extensions.toc'  # 自动生成目录
        ])  # 修改blog.content内容为html

        return post


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'blogs/comment.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        post = get_object_or_404(Post, pk=target)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = post
            instance.save()
            succeed = True
            return redirect('/blogs/post/' + str(post.id))
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'errors': comment_form.errors,
        }

        return self.render_to_response(context)


# tag's list
def tag_list(request, tag_id):
    posts = Post.objects.filter(tags__id=tag_id).select_related('category')
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    menus = Category.get_menus()

    return render(request, 'blogs/list.html', {'posts': posts, 'menus': menus, 'page_obj':page_obj})
