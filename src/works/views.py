from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Stage
from django.core import serializers
from .serializers import StageListSerializer, StageDetailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404, HttpResponse
from rest_framework import generics, routers, serializers, viewsets
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
            
    return HttpResponse(msg)



class StageList(generics.ListCreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageListSerializer


# ViewSets define the view behavior.
class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageListSerializer

    # 新增代码
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StageDetail(APIView):
    """详情视图"""

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
            # 序列化器将持有的数据反序列化后，
            # 保存到数据库中
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stage = self.get_object(pk)
        stage.delete()
        # 删除成功后返回204
        return Response(status=status.HTTP_204_NO_CONTENT)
