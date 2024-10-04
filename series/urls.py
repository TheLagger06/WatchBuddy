from django.urls import path
from . import views


urlpatterns = [
    path('series/', views.series_list, name='series_list'),  # List of series
    path('series/<int:series_id>/', views.series_detail, name='series_detail'),
    path('search/', views.search_series, name='search_series'),  # Search series 
]

