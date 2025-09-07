# Movie Recommender System

A Flask-based movie recommendation system that suggests similar movies based on movie contents. The system uses the top 3,500 movies selected from an original dataset of 10,000 movies.

## Live Demo
- [Movie Recommender on Render](https://movierecommender-88vk.onrender.com/)

<p align="center">
  <a href="https://github.com/user-attachments/assets/873ec688-5e8d-4cce-8ecb-40a73f3163e3">
    <img src="https://github.com/user-attachments/assets/873ec688-5e8d-4cce-8ecb-40a73f3163e3" alt="Movie Recommender Demo" width="800"/>
  </a>
</p>

## Features
- Movie recommendations based on content similarity
- Integration with TMDB API for movie posters and details
- Flask backend + frontend in one lightweight app
- Deployed on Render for easy access

## Tech Stack
- Backend: Flask
- Frontend: Jinja2 templates (HTML, CSS, JS)
- Data: Pickled similarity matrix & movies (preprocessed in Jupyter Notebook)
- API: TMDB API for movie posters and details
- Deployment: Render

## Sources
- Dataset: [Full TMDB Movies Dataset 2024 (1M Movies)](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/data)
- Movie details: [TMDB](https://www.themoviedb.org/)

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python app.py
```

Visit http://localhost:5000 in your web browser to use the application.

## Logo
[![movie-night-black.png](https://i.postimg.cc/1XznQnqr/movie-night-black.png)](https://postimg.cc/tZLCdgDs)
