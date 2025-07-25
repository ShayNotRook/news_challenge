import django_filters
from django.db.models import Q

from .models import News


class NewsFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr="icontains", label="Tag name")
    keywords_included = django_filters.CharFilter(method='filter_included', label="Include Keyword (comma separated)")
    keywords_excluded = django_filters.CharFilter(method='filter_excluded', label="Exlude Keywords (comma separated)")
    
    class Meta:
        model = News
        fields = []
        
        
    def filter_included(self, queryset, name, value: str):
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword) | Q(body_text__icontains=keyword)
        
        return queryset.filter(query)
    
    def filter_excluded(self, queryset, name, value):
        keywords = [k.strip() for k in value.split(',') if k.strip()]
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword) | Q(body_text__icontains=keyword)
        
        return queryset.exclude(query)