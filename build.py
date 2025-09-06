import os
from app import app, movies
import requests
from flask import url_for
import shutil

def save_page(url, filename):
    with app.test_client() as client:
        response = client.get(url)
        os.makedirs(os.path.dirname(f'build/{filename}'), exist_ok=True)
        with open(f'build/{filename}', 'wb') as f:
            f.write(response.data)

def build_static_site():
    # Create build directory
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    # Copy static files
    if os.path.exists('static'):
        shutil.copytree('static', 'build/static')

    # Generate index page
    save_page('/', 'index.html')

    # Generate movie detail pages for first 100 movies (for testing)
    for index, row in movies.head(100).iterrows():
        movie_id = row['id']
        save_page(f'/movie/{movie_id}', f'movie/{movie_id}/index.html')

    print("Static site built successfully in 'build' directory")

if __name__ == '__main__':
    # Set the application context
    with app.app_context():
        app.config['SERVER_NAME'] = 'localhost'  # Required for url_for to work
        build_static_site()
