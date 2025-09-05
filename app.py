import pickle
import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

per_page = 20

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    backdrop_path = "https://image.tmdb.org/t/p/w500/" + data['backdrop_path']
    return poster_path, backdrop_path

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

@app.route('/')
def home():
    # Get the page number from the query parameters, default to 1
    page = request.args.get('page', 1, type=int)
    
    # Calculate pagination
    total_movies = len(movies)
    total_pages = (total_movies + per_page - 1) // per_page
    
    # Calculate start and end indices for the current page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_movies)
    
    # Get only the movies for the current page
    paginated_movies = []
    for index in range(start_idx, end_idx):
        row = movies.iloc[index]
        movie_id = row.id
        poster, backdrop = fetch_poster(movie_id)
        paginated_movies.append({
            'index': index,
            'title': row.title,
            'poster_url': poster,
            'backdrop_url': backdrop,
            'genres': row.genres if 'genres' in row else ''
        })
    
    return render_template('home.html', 
                         movies=paginated_movies,
                         current_page=page,
                         total_pages=total_pages)

@app.route('/recommend/<int:movie_code>')
def get_recommendations(movie_code):
    recommendations = recommend(movie_code)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    page = request.args.get('page', 1, type=int)

    if not query:
        # If no query, redirect to home page with pagination
        return home()
    
    # Filter movies based on the search query
    search_results = []
    for index, title in enumerate(movies['title'].values):
        if query in title.lower():
            movie_id = movies.iloc[index].id
            poster, backdrop = fetch_poster(movie_id)
            search_results.append({
                'index': index,
                'title': title,
                'poster_url': poster,
                'backdrop_url': backdrop,
                'genres': movies.iloc[index].genres if 'genres' in movies.iloc[index] else ''
            })
    
    # Calculate pagination for search results
    total_results = len(search_results)
    total_pages = (total_results + per_page - 1) // per_page
    
    # Get the current page's results
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_results)
    paginated_results = search_results[start_idx:end_idx]
    
    return render_template('search.html', 
                         movies=paginated_results,
                         current_page=page,
                         total_pages=total_pages,
                         query=query)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
