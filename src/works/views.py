from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Stage
from django.core import serializers
from .serializers import StageListSerializer, StageDetailSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


def index(request):
    return render(request, 'works/index.html')


def story_ist(request):
    return render(request, 'works/story_list.html')


def story_detail(request):
    return render(request, 'works/story_detail.html')


def stage_list_json(request):
    stages = Stage.objects.all()
    serializer = StageListSerializer(stages, many=True)
    return JsonResponse(serializer.data, safe=False)


def stage_detail(request, stage_id):
    stage = Stage.objects.get(pk=stage_id)
    return render(request, 'works/stage_detail.html', {'stage': stage})


def stage_json(request, stage_id):
    stage = Stage.objects.get(pk=stage_id)
    stage_json = serializers.serialize('json', stage.content)
    print(stage_json)

    return JsonResponse(stage_json)


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


def editor(request):
    return render(request, 'works/stage_editor.html')
