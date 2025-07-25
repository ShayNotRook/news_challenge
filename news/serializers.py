from rest_framework.serializers import ModelSerializer

from .models import News, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'