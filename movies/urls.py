from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:movie_id>/', views.movies_detail, name='movies_detail'),  # URL for movie details
    path('search/', views.search_movies, name='search_movies'),  # URL for searching movies
    path('movies/', views.movies_list, name='movies_list'),  # URL for listing movies
]

