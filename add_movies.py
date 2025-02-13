import os
import django
import json
import requests
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GTMoviesApp.settings')
django.setup()
load_dotenv()

from movies.models import Movie


def add_movies():

    movie_api_key = os.getenv('MOVIE_API_KEY')
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&vote_count.gte=500"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + movie_api_key
    }
    new_movie_list = []
    
    for i in range(1, 11):
        response = requests.get(url + "&page="+ str(i), headers=headers)
        if response.status_code == 200:
            json = response.json()
            results = json['results']
            for movie in results:
                image_path = (str(movie['title']).replace(' ', '_').lower())+'.jpg'
                image_url = "https://image.tmdb.org/t/p/original"+str(movie['poster_path'])
                image_response = requests.get(image_url)
                if (image_response.status_code == 200):
                    os.path.join('media', 'movie_images', image_path)
                    with open(os.path.join('media', image_path), 'wb') as file:
                        file.write(image_response.content)
                new_movie_list.append(Movie(
                    name=movie['title'], 
                    description=movie['overview'],
                    image=image_path,
                    price=0
                ))
    
    # ! LEAVE THIS COMMENTED OUT UNLESS YOU NEED TO FILL THE DATABASE !
    Movie.objects.bulk_create(new_movie_list)
    # ! LEAVE THIS COMMENTED OUT UNLESS YOU NEED TO FILL THE DATABASE !

    
if __name__ == '__main__':
    add_movies() 