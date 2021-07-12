from django.urls import path
from . import views
import base

app_name = 'search'

urlpatterns = [
    path('', views.SearchResultView.as_view(), name='result'),
]