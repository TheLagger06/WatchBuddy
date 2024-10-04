from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm
import requests
import os

BASE_URL = 'https://api.themoviedb.org/3'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user to the database
            login(request, user)  # Log the user in after successful registration
            return redirect('home')  # Redirect to the home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

from django.views.generic import TemplateView

class HomePage(TemplateView):
    """Displays home page"""
    template_name = 'index.html'


def index(request):
    try:
        movies_response = requests.get(f"{BASE_URL}/movie/popular?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US")
        if movies_response.status_code == 200:
            recent_movies = movies_response.json().get('results', [])[:20]
        else:
            recent_movies = []
            print(f"Error fetching movies: {movies_response.status_code}")
    except requests.exceptions.RequestException as e:
        recent_movies = []
        print(f"Movies request failed: {e}")

    try:
        series_response = requests.get(f"{BASE_URL}/tv/popular?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US")
        if series_response.status_code == 200:
            recent_series = series_response.json().get('results', [])[:20]
        else:
            recent_series = []
            print(f"Error fetching series: {series_response.status_code}")
    except requests.exceptions.RequestException as e:
        recent_series = []
        print(f"Series request failed: {e}")

    try:
        trending_response = requests.get(f"{BASE_URL}/trending/all/day?api_key={os.environ.get('TMDB_API_KEY')}")
        if trending_response.status_code == 200:
            trending_items = trending_response.json().get('results', [])[:20]
        else:
            trending_items = []
            print(f"Error fetching trending items: {trending_response.status_code}")
    except requests.exceptions.RequestException as e:
        trending_items = []
        print(f"Trending request failed: {e}")

    request.session['recent_movies'] = recent_movies
    request.session['recent_series'] = recent_series

    latest_items = recent_movies + recent_series + trending_items
    return render(request, 'index.html', {
        'latest_items': latest_items,
        'trending_items': trending_items,
        'recent_movies': recent_movies,
        'recent_series': recent_series
    })
