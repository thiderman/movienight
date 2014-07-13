import tmdb3
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from movienight.mn.utils import serialize_movie
from movienight.mn.utils import js_template


class MovieNightView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MovieNightView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'index.html', {})

    @csrf_exempt
    def post(self, request):
        post = request.POST

        if 'search' in post:
            res = tmdb3.searchMovie(post['search'])
            movies = [serialize_movie(m) for m in res[:20]]

            ret = {
                'movies': movies
            }

        ret['template'] = js_template('searchresult.html')
        return HttpResponse(json.dumps(ret), content_type="application/json")


class MovieNightMovie(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MovieNightMovie, self).dispatch(*args, **kwargs)

    def get(self, request, movie_id):
        movie = tmdb3.Movie(movie_id)
        return render(
            request,
            'movie.html',
            {'movie': serialize_movie(movie, True)}
        )
