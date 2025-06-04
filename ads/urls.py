from django.urls import path
from . import views
from .views import (
    HomeView, AdDetailView, AdUpdateView, AdDeleteView,
    UserAdListView, CategoryAdListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('ad/new/', views.AdCreateView.as_view(), name='ad-create'),
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
    path('user/<str:username>/', UserAdListView.as_view(), name='user-ads'),
    path('category/<str:category>/', CategoryAdListView.as_view(), name='category-ads'),
    path('search/', views.search_ads, name='search-ads'),
]
