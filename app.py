import pickle
import os
from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd

app = Flask(__name__)

per_page = 20
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, TMDB_API_KEY)
    data = requests.get(url)
    data = data.json()
    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    backdrop_path = "https://image.tmdb.org/t/p/w500/" + data['backdrop_path']
    return poster_path, backdrop_path

def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id, TMDB_API_KEY)
    data = requests.get(url)
    data = data.json()
    data['full_poster_path'] = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    data['full_backdrop_path'] = "https://image.tmdb.org/t/p/w500/" + data['backdrop_path']
    data['genres'] = ', '.join([genre['name'] for genre in data.get('genres', [])])
    return data

def recommend(index):
    # Get similarity scores for this movie with all other movies
    similarity_scores = similarity[index]
    # Convert to list of tuples: (index, similarity_score)
    distances = sorted(list(enumerate(similarity_scores)), reverse=True, key=lambda x: x[1])
    recommendations = []
    
    for i in distances[1:9]:
        movie_data = movies.iloc[i[0]]
        movie_id = movie_data.id
        poster, backdrop = fetch_poster(movie_id)
        recommendations.append({
            'title': movie_data.title,
            'poster_url': poster,
            'backdrop_url': backdrop,
            'genres': movie_data.genres if 'genres' in movie_data else ''
        })
    
    return recommendations

# Load the movies and similarity matrices
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def get_random_backdrop():
    # Get a random movie from the dataset
    random_movie = movies.sample(n=1).iloc[0]
    movie_id = random_movie['id']
    _, backdrop = fetch_poster(movie_id)
    return backdrop

@app.route('/')
def home():
    search_query = request.args.get('query', '').strip()
    page = request.args.get('page', 1, type=int)
    
    # Get a random backdrop for the hero section
    backdrop_url = get_random_backdrop()
    
    filtered_movies = movies
    if search_query:
        # Search only in titles
        filtered_movies = movies[
            movies['title'].str.lower().str.contains(search_query.lower())
        ]
    
    # Calculate pagination
    total_movies = len(filtered_movies)
    total_pages = max((total_movies + per_page - 1) // per_page, 1)
    
    # Ensure page is within bounds
    page = min(max(1, page), total_pages)
    
    # Calculate start and end indices for the current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_movies)
    
    # Get only the movies for the current page
    paginated_movies = []
    for index in range(start_idx, end_idx):
        row = filtered_movies.iloc[index]
        movie_id = row.id
        try:
            poster, backdrop = fetch_poster(movie_id)
            paginated_movies.append({
                'index': filtered_movies.index[index],
                'title': row.title,
                'poster_url': poster,
                'backdrop_url': backdrop,
                'genres': row.genres if 'genres' in row else '',
                'vote_average': row.vote_average if 'vote_average' in row else None
            })
        except:
            continue  # Skip if poster fetch fails
    
    return render_template('home.html', 
                         movies=paginated_movies,
                         current_page=page,
                         total_pages=total_pages,
                         search_query=search_query,
                         hero_backdrop=backdrop_url)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return render_template('home.html', movies=[], current_page=1, total_pages=1)
    
    # Search through movies
    search_results = []
    for index, row in movies.iterrows():
        if query in row.title.lower():
            movie_id = row.id
            poster, backdrop = fetch_poster(movie_id)
            search_results.append({
                'index': index,
                'title': row.title,
                'poster_url': poster,
                'backdrop_url': backdrop,
            })
    
    return render_template('home.html', 
                         movies=search_results,
                         current_page=1,
                         total_pages=1,
                         is_search=True)

@app.route('/movie/detail/<int:movie_code>')
def movie_detail(movie_code):
    movie_data = movies.iloc[movie_code]
    movie_id = movie_data.id
    movie_data = fetch_movie_details(movie_id)
    recommendations = recommend(movie_code)
    return render_template('detail.html', movie_data=movie_data, recommendations=recommendations)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
