from django.urls import path
from .views import scraper,contentRag

urlpatterns = [
    path('',scraper, name='scraper'),
    path('contentRag',contentRag, name='contentRag'),
]
