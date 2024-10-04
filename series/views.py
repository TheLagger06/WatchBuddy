import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import os

BASE_URL = 'https://api.themoviedb.org/3'

def search_series(request):
    query = request.GET.get('q', '')
    results = []

    if query:  # Only fetch results if there is a query
        url = f"{BASE_URL}/search/tv?api_key={os.environ.get('TMDB_API_KEY')}&query={query}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results', [])
        else:
            # Handle errors here, you might want to log this or show a message
            results = []

    return render(request, 'series/search_results.html', {'results': results, 'query': query})

def get_series_details(series_id):
    url = f'{BASE_URL}/tv/{series_id}?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def get_cast(series_id):
    url = f"{BASE_URL}/tv/{series_id}/credits?api_key={os.environ.get('TMDB_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 200:
        cast_data = response.json()
        directors = [member for member in cast_data['crew'] if member['job'] == 'Producer']
         
        return {
            'cast': cast_data['cast'],
            'directors': directors,
        }
     
    return {'cast': [], 'directors': []}  # Return empty lists if there's an error

def get_trailer_key(series_id):
    url = f"{BASE_URL}/tv/{series_id}/videos?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    video_details = requests.get(url).json()
    for video in video_details.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return video['key']
    return None

def get_ratings(series_id):
    url = f"{BASE_URL}/tv/{series_id}/content_ratings?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    ratings_details = requests.get(url).json()

    for release in ratings_details.get('results', []):
        if release['iso_3166_1'] == 'GB':  # Check for GB ratings
            ratings = release.get('rating', 'N/A')  # Get the rating or 'N/A'
            return ratings

    return 'N/A'

def get_series_seasons(series_id):
    url = f"{BASE_URL}/tv/{series_id}?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    response = requests.get(url)
    return response.json().get('seasons', []) if response.status_code == 200 else []



def get_season_episodes(series_id, season_number):
    url = f"{BASE_URL}/tv/{series_id}/season/{season_number}?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('episodes', [])
    return []  # Return empty list if there was an error

def series_detail(request, series_id):
    series_detail = get_series_details(series_id)  # Fetch series details
    cast_details = get_cast(series_id)  # Get cast and director details
    trailer_key = get_trailer_key(series_id)  # Get trailer key
    ratings = get_ratings(series_id)  # Get ratings
    
    # Fetch all seasons details
    seasons = series_detail.get('seasons', [])
    
    # Get season number from the request, default to 1 if not provided
    selected_season_number = request.GET.get('season_number', 1)
    
    # Fetch the episodes for the selected season
    episodes = get_season_episodes(series_id, selected_season_number)
    

    return render(request, 'series/series_detail.html', {
        'series_details': series_detail,
        'cast': cast_details['cast'],
        'trailer_key': trailer_key,
        'directors': cast_details['directors'],
        'rating': ratings,
        'seasons': seasons,
        'selected_season_number': selected_season_number,
        'episodes': episodes,  # Pass episodes to the template
    })


def series_list(request):
    # Retrieve data from session
    recent_series = request.session.get('recent_series', [])

    # Get today's date
    today = datetime.today().strftime('%Y-%m-%d')
   
    # Fetch the airing series
    airing_today_response = requests.get(f"{BASE_URL}/discover/tv?api_key={os.environ.get('TMDB_API_KEY')}&air_date.gte={today}&air_date.lte={today}&sort_by=popularity.desc&sort_by=vote_count.desc")

    airing_today_series = airing_today_response.json().get('results', [])[:20]

    
    # Fetch the top-rated series
    top_rated_response = requests.get(f"{BASE_URL}/tv/top_rated?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US")
    top_rated_series = top_rated_response.json().get('results', [])[:20]

    return render(request, 'series/series_list.html', {
        'airing_today_series': airing_today_series,
        'top_rated_series': top_rated_series,
        'recent_series': recent_series,

          })