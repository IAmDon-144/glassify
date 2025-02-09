import django_filters
from  django_filters import DateFilter,CharFilter
from .models import Glasses

class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',lookup_expr='icontains')

    
    class Meta:
        model = Glasses
        fields = ['title']

        
