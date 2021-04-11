
from django.urls import path
from .views import (
   ArticleListView,
   ArticleDetailView,
)
from . import views

urlpatterns = [
    path('', views.index, name='articels-home'),
    path('show/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),

]
