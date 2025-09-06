from flask_frozen import Freezer
from app import app, movies
import pandas as pd

# Configure the app for static generation
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
freezer = Freezer(app)

# Define URL generators for Frozen-Flask
@freezer.register_generator
def index():
    yield {}  # Just the main page

@freezer.register_generator
def movie_detail():
    # Generate URLs for all movies in your dataset
    for index, row in movies.iterrows():
        yield {'movie_id': row['id']}

@freezer.register_generator
def recommend():
    # Generate URLs for recommendations
    for index, row in movies.head(10).iterrows():  # Limit to first 10 for testing
        yield {'movie_id': row['id']}

if __name__ == '__main__':
    freezer.freeze()
