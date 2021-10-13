from django.shortcuts import render
from .models import Stage
from .serializers import StageSerializer, StageListSerializer, StageDetailSerializer

from simple_history.utils import update_change_reason

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.http import Http404, HttpResponse, request
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from works.permissions import IsAdminUserOrReadOnly
import json


def index(request):
    return render(request, 'works/index.html')


# 检查标题是否重复
def check_title(request):
    allow = 'yes'
    if request.method == "POST":
        data = json.loads(request.body)
        stage = Stage.objects.filter(title=data['title']).first()
        if stage:
            allow = 'no'

    return HttpResponse(allow)

def add_star(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        stage = Stage.objects.filter(id=data['stage_id']).filter()
        



class StageWidgetListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


# ViewSets define the view behavior.
class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

    # permission_classes = [IsAuthenticated,]
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        type = self.request.query_params.get('type', None)
        if type is not None:
            self.pagination_class = StageWidgetListPagination
            self.queryset = self.queryset.filter(type=type)
        return self.queryset

    # 新增
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# 作者的作品列表
class StageListByAuthor(ListAPIView):
    serializer_class = StageListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user_id = self.kwargs['user_id']
        user = self.request.user
        return Stage.objects.filter(owner_id = user_id)


class StageDetail(APIView):
    """详情视图"""
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_object(self, pk):
        """获取单个文章对象"""
        try:
            # pk 即主键，默认状态下就是 id
            return Stage.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        stage = self.get_object(pk)
        serializer = StageDetailSerializer(stage)
        # 返回 Json 数据
        return Response(serializer.data['content'])

    def put(self, request, pk):
        stage = self.get_object(pk)
        serializer = StageDetailSerializer(stage, data=request.data)
        # 验证提交的数据是否合法
        # 不合法则返回400
        if serializer.is_valid():
            # 序列化器将持有的数据反序列化
            # 保存到数据库中
            serializer.save()
            # 在history中记录更改原因
            if 'reason' in request.data:
                update_change_reason(stage, request.data['reason'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stage = self.get_object(pk)
        stage.delete()
        # 删除成功后返回204
        return Response(status=status.HTTP_204_NO_CONTENT)
