import pickle
import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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
    # Create a list of tuples (id, title) for the dropdown
    movie_list = [(index, title) for index, title in enumerate(movies['title'].values)]
    return render_template('home.html', movies=movie_list)

@app.route('/recommend/<int:movie_code>')
def get_recommendations(movie_code):
    recommendations = recommend(movie_code)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return render_template('home.html', movies=[(index, title) for index, title in enumerate(movies['title'].values)])
    
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
    
    return render_template('search.html', recommendations=search_results)

@app.route('/random')
def random_recommendation():
    return render_template('random.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
