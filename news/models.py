from django.db import models

# Create your models here.



class News(models.Model):
    TAGS_CHOICES = [
        ("ENTERTAINMENT", "Entertainment"),
        ("SPORTS", "Sports"),
        ("POLITICS", "Politics")
    ]        
    
    _title = models.CharField(max_length=250)
    _body_text = models.TextField(max_length=1000)
    _tags = models.CharField(choices=TAGS_CHOICES)
    
    def __str__(self):
        return f"{self.title} - {self.body_text[:10]}"
    
    
    @property
    def title(self):
        return self._title
    
    @property
    def body(self):
        return self._body_text
    
    @classmethod
    def filter_by_tag(cls, tag: str):
        if tag:
            return cls.objects.filter(_tags=tag)
    
    def all_news(self):
        return self.objects.all()