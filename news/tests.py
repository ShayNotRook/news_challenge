from django.test import TestCase
from .models import News, Tag
from .filters import NewsFilter
from django.db.models import QuerySet



class NewsFilterTests(TestCase):
    def setUp(self):
        # Tags
        tech = Tag.objects.create(name='Tech')
        heatlh = Tag.objects.create(name='Health')
        
        
        # News
        self.n1 = News.objects.create(title="New Macbook", body_text="Revealing of new silicon chip")
        self.n1.tags.add(tech)
        
        self.n2 = News.objects.create(title="Cancer Vaccine", body_text="Researchers published new studies regarding cancer cells")
        self.n2.tags.add(heatlh)
        
        self.n3 = News.objects.create(title="Diagnose chip", body_text="You could now fully diagnose your body issues using an app")
        self.n3.tags.add(tech, heatlh)
        
        # Without adding any of the tags
        self.n4 = News.objects.create(title="Test4", body_text="test body4")
        
        
    
    # Filter tests
    def test_include_keywords_filter(self):
        params = {'keywords_included': 'Diagnose, Cancer, New Macbook'}
        qs = NewsFilter(data=params, queryset=News.objects.all()).qs
        
        titles = set(qs.values_list('title', flat=True))
        self.assertIn("New Macbook", titles)    
        self.assertIn("Cancer Vaccine", titles)    
        self.assertIn("Diagnose chip", titles)
        self.assertNotIn("Test4", titles)    
        
        
    def test_exclude_keywords_filter(self):
        params = {'keywords_excluded': 'test'}
        qs = NewsFilter(data=params, queryset=News.objects.all()).qs
        
        titles = set(qs.values_list('title', flat=True))
        self.assertIn("New Macbook", titles)
        self.assertIn("Cancer Vaccine", titles)
        self.assertIn("Diagnose chip", titles)
        self.assertNotIn("Test4", titles)
        
        
    def test_by_tag_name(self):
        param = {'tags': "Tech, Health"}
        qs = NewsFilter(data=param, queryset=News.objects.all()).qs
        
        titles = set(qs.values_list('title', flat=True)) 
        self.assertIn("New Macbook", titles)
        self.assertIn("Cancer Vaccine", titles)
        self.assertIn("Diagnose chip", titles)
        self.assertNotIn("Test4", titles)
        