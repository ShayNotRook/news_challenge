from typing import Union

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"


class News(models.Model):

    title = models.CharField(max_length=250)
    body_text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = "News"
    
    def __str__(self):
        return f"{self.title} - {self.body_text[:10]}"
    
