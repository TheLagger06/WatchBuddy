from django.shortcuts import render
import requests
import os

BASE_URL = 'https://api.themoviedb.org/3'

def search_movies(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Use TMDb API to search for movies
        url = f'https://api.themoviedb.org/3/search/movie?api_key={os.environ.get('TMDB_API_KEY')}&query={query}'
        response = requests.get(url).json()
        if response.get('results'):
            results = response['results']

    return render(request, 'movies/search_results.html', {'results': results})

def get_movies_details(movie_id):
    url = f'{BASE_URL}/movie/{movie_id}?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US'
    response = requests.get(url)
    return response.json()

def get_cast(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={os.environ.get('TMDB_API_KEY')}"
    response = requests.get(url)
    if response.status_code == 200:
        cast_data = response.json()
        directors = [member for member in cast_data['crew'] if member['job'] == 'Director']
        writers = [member for member in cast_data['crew'] if member['department'] == 'Writing']
        return {
            'cast': cast_data['cast'],
            'directors': directors,
            'writers': writers
        }
    return {'cast': [], 'directors': [], 'writers': []}  # Return empty lists if there's an error

def get_trailer_key(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/videos?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    video_details = requests.get(url).json()
    for video in video_details.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return video['key']
    return None


def get_certifications(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/release_dates?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US"
    certifications_details = requests.get(url).json()
    for release in certifications_details.get('results', []):
            if release['iso_3166_1'] == 'GB':  # Check for GB certifications
                certifications = release.get('release_dates', [])
                if certifications:
                    return certifications[0].get('certification', 'N/A')  # Return the certification or 'N/A'
    return 'N/A'      

def movies_detail(request, movie_id):
    movies_details = get_movies_details(movie_id)  # Fetch movie details
    cast_details = get_cast(movie_id)  # Get cast and director details
    trailer_key = get_trailer_key(movie_id)  # Get trailer key
    certifications = get_certifications(movie_id)  # Get certifications

    runtime = movies_details.get('runtime', 0)
    hours = runtime // 60
    minutes = runtime % 60
    movies_details['runtime_formatted'] = f"{hours}h {minutes}m"  # Format the runtime
    
    return render(request, 'movies/movies_details.html', {
        'movies_details': movies_details,
        'cast': cast_details['cast'],
        'trailer_key': trailer_key,
        'directors': cast_details['directors'],  # Pass directors to the template
        'certification': certifications,  # Pass certifications to the template
        'writers': cast_details['writers'],  # Pass writers to the template
    })



def movies_list(request):
    # Retrieve data from session
    recent_movies = request.session.get('recent_movies', [])

    # Fetch the upcoming movies
    upcoming_response = requests.get(f'https://api.themoviedb.org/3/movie/upcoming?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US&page=1')
    upcoming_movies = upcoming_response.json().get('results', [])[:20]

    # Fetch the top-rated movies
    top_rated_response = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key={os.environ.get('TMDB_API_KEY')}&language=en-US')
    top_rated_movies = top_rated_response.json().get('results', [])[:20]

    return render(request, 'movies/movies_list.html', {
        'upcoming_movies': upcoming_movies,
        'top_rated_movies': top_rated_movies,
        'recent_movies': recent_movies,
    })