from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

REPO_NAME = "Movie-Recommender-System"
AUTHOR_USER_NAME = "mmmudmi"
LIST_OF_REQUIREMENTS = [
    'Flask>=2.0.1',
    'pandas>=2.0.0',
    'requests>=2.26.0',
    'gunicorn>=20.1.0',
    'numpy>=1.24.0',
    'scikit-learn>=1.0.0'
]


setup(
    name="movie-recommender",
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="A Flask-based Movie Recommender System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="mmmudmi@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)