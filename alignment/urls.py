# alignment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',              views.index,       name='alignment-index'),
    path('api/align/',    views.AlignView.as_view(),   name='api-align'),
    path('api/history/',  views.HistoryView.as_view(), name='api-history'),
]