from django.urls import path
from . import views
from .views import (
    HomeView, AdDetailView, AdUpdateView, AdDeleteView,
    UserAdListView, CategoryAdListView
)

urlpatterns = [

    # Главная страница: список всех объявлений
    path('', HomeView.as_view(), name='home'), 

    # Страница конкретного объявления (GET)
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad-detail'),

    # Создание нового объявления:
    # GET: отрисовка формы
    # POST: передача данных формы + медиа
    path('ad/new/', views.AdCreateView.as_view(), name='ad-create'),

    # Редактирование объявления:
    # GET: отрисовка заполненной формы
    # POST: передача данных формы + изменения медиа
    path('ad/<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),

    # Удаление объявления:
    # GET: подтверждение удаления 
    # POST: фактически удаление записи
    path('ad/<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),

    # Список объявлений конкретного пользователя (GET)
    path('user/<str:username>/', UserAdListView.as_view(), name='user-ads'),

    # Список объявлений по категории (GET)
    path('category/<str:category>/', CategoryAdListView.as_view(), name='category-ads'),

    # Поиск объявлений (GET с параметрами в строке запроса)
    path('search/', views.search_ads, name='search-ads'),
]
