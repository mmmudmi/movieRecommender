from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -

REPO_NAME = "movieRecommender"
AUTHOR_USER_NAME = "mmmudmi"
LIST_OF_REQUIREMENTS = [
    'flask>=2.3.3',
    'requests>=2.31.0',
    'numpy>=1.24.3',
    'pandas>=2.0.3',
    'scikit-learn>=1.3.0',
    'gunicorn>=21.2.0',
    'Frozen-Flask>=0.18'
]


setup(
    name=REPO_NAME,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="Movie Recommender System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="mmmudmi@gmail.com",
    packages=["movieRecommender"],
    package_dir={"movieRecommender": "."},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)