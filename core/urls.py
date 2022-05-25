""" core/urls.py """
from django.urls import path
from core import views


urlpatterns = [
  path('', views.index, name = 'index'),
  path('search/name/<str:name>/', views.search_data, name='data-detail'),
  path('api/', views.ContentLinkTextAPIView.as_view(), name='api-content-view'),
]
 