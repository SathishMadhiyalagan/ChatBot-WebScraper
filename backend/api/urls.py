from django.urls import path
from .views import add_text_content,handle_query

urlpatterns = [
    path('', add_text_content),
    path('query',handle_query)
]
