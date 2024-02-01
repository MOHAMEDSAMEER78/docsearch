# paragraph_search/models.py

from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=255, unique=True)

class Paragraph(models.Model):
    content = models.TextField()
    words = models.ManyToManyField(Word)
    unique_id = models.CharField(max_length=100, unique=True,null=True)
