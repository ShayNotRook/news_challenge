from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend

from .filters import NewsFilter
from .models import News
from .serializers import NewsSerializer



class GetAllNews(ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    