from django.urls import path
from .views import add_paragraphs, search_paragraphs, get_all_paragraphs

urlpatterns = [
    path('add_paragraph/', add_paragraphs, name='add_paragraph'),
    path('search_paragraphs/', search_paragraphs, name='search_paragraphs'),
    path('get_all_paragraphs/', get_all_paragraphs, name='get_all_paragraphs'),
]
