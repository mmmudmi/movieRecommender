from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -

REPO_NAME = "movieRecommender"
AUTHOR_USER_NAME = "mmmudmi"
LIST_OF_REQUIREMENTS = ['streamlit']


setup(
    name=REPO_NAME,
    version="0.0.1",
    author=AUTHOR_USER_NAME,
    description="Movie Recommender System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="mmmudmi@gmail.com",
    packages=[REPO_NAME],
    python_requires=">=3.7",
    install_requires=LIST_OF_REQUIREMENTS
)