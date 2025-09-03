import pickle
import requests
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

movies = pickle.load(open("movies.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# TMDB API key - replace with your actual API key
api_key = "1acee36263c35268f88f2e5defb49492"

def fetch_poster(tmdbId):
    # Fetch movie poster from TMDB API
    url = f"https://api.themoviedb.org/3/movie/{tmdbId}?api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return ["https://image.tmdb.org/t/p/w500" + data['poster_path'], 
                    "https://image.tmdb.org/t/p/w500" + data['backdrop_path']]
    except:
        pass
    return None

def recommend_by_movie_id(movie_id):
    index = movies[movies['id']==movie_id].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommendations = []
    for i in distance[1:9]:
        movie_info = movies.iloc[i[0]]
        recommendations.append({
            'id': movie_info['id'],
            'title': movie_info['title']
        })
    recommendations = sorted(recommendations, key=lambda x: x['title'])
    return pd.DataFrame(recommendations)

@app.route('/')
def home():
    # Get list of movies for the dropdown
    movie_list = list(zip(movies['id'].tolist(), movies['title'].tolist()))
    return render_template('home.html', movies=movie_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_id = int(request.form['movie'])
    recommendations = recommend_by_movie_id(movie_id)
    # Add poster URLs to recommendations
    recommendations['poster_url'], recommendations['backdrop_url'] = zip(*recommendations['id'].apply(fetch_poster))

    return render_template('recommendations.html', 
                         recommendations=recommendations.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)



#/Users/mudmi/Desktop/movieRecommender/.venv/bin/python app.py run it