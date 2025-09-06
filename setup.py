from setuptools import setup, find_packages

setup(
    name="movieRecommender",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask>=2.3.3',
        'requests>=2.31.0',
        'numpy>=1.24.3',
        'pandas>=2.0.3',
        'scikit-learn>=1.3.0',
        'gunicorn>=21.2.0',
        'Frozen-Flask>=0.18'
    ],
    python_requires=">=3.8,<3.12"
)