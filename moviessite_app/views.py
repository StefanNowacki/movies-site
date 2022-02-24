from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .models import Movie, ActorMovie, Comment, Director, Actor, RATING


# main page conteins movie search engine
class Movies(View):

    def get(self, request):
        movie_name = request.GET.get('movie_name')
        if movie_name:
            movies = Movie.objects.filter(title__icontains=movie_name).order_by('rating')
        else:
            movies = Movie.objects.all().order_by('rating')
        return render(request, 'main_page.html', {'movies': movies})


# Showing movie details and comments about the movie. You can also add new comment.
class MovieDetails(View):

    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        actors = ActorMovie.objects.filter(movie_id=movie_id)
        comments = Comment.objects.filter(movie_id=movie_id)
        return render(request, 'movie_details.html', {'movie': movie,
                                                      'actors': actors,
                                                      'comments': comments})

    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        Comment.objects.create(description=request.POST.get('comment'),
                               movie_id=movie.id)
        return redirect(f'/movie_details/{movie_id}')


# admin view conteins movie search engine
class AdminView(View):

    # def __init__(self, request):
    #     self.user = request.user

    # @login_required
    def get(self, request):

        if self.request.user.is_superuser:
            movie_name = request.GET.get('movie_name')
            if movie_name:
                movies = Movie.objects.filter(title__icontains=movie_name).order_by('rating')
            else:
                movies = Movie.objects.all().order_by('rating')
            return render(request, 'admin_view.html', {'movies': movies})
        else:
            raise PermissionError


class DeleteMovie(View):

    def get(self, request, movie_id):
        Movie.objects.get(pk=movie_id).delete()
        return HttpResponse('Movie has been deleted')


class EditMovie(View):

    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        directors = Director.objects.all()
        actors = Actor.objects.all()
        return render(request, 'edit_movie.html', {'movie': movie,
                                                   'directors': directors,
                                                   'actors': actors,
                                                   'ratings': RATING})

    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        movie.title = request.POST.get('title')
        movie.director = Director.objects.get(pk=int(request.POST.get('director')))
        # print(request.POST.getlist('actors[]'))
        actors = request.POST.getlist('actors')
        # print(actors)
        for actor in actors:
            if ActorMovie.objects.filter(actor_id=actor, movie_id=movie_id).exists():
                # print(actor)
                messages.error(request, 'actor already exist in this movie')
            else:
                ActorMovie.objects.create(actor_id=actor, movie_id=movie_id)
        movie.rating = request.POST.get('rating')
        movie.description = request.POST.get('description')
        movie.save()
        return redirect(f'/movie_details/{movie_id}')


#allows you to edit actors in movies and makes sure that actor is not duplicated in the movie. It will work only when you are log in
class EditMovieActors(View):

    def get(self, request, movie_id):
        if self.request.user.is_superuser:
            movie = Movie.objects.get(pk=movie_id)
            movie_actors = ActorMovie.objects.filter(movie_id=movie_id)
            actors = Actor.objects.all()
            return render(request, 'edit_movie_actors.html', {'movie': movie,
                                                              'actors': actors,
                                                              'movie_actors': movie_actors})

    def post(self, request, movie_id):
        actor_id = int(request.POST.get('actor'))
        if ActorMovie.objects.filter(actor_id=actor_id, movie_id=movie_id).exists():
            messages.error(request, 'actor already exist in this movie')
        else:
            ActorMovie.objects.create(movie_id=movie_id, actor_id=actor_id)
        return HttpResponseRedirect(request.path_info)


#allows you to remove actors from movies and makes sure that actor is not duplicated in the movie.It will work only when you are log in
class DeleteMovieActors(View):

    def get(self, request, movie_actor_id):
        actor = ActorMovie.objects.get(pk=movie_actor_id)
        movie_id = actor.movie_id
        actor.delete()
        # return redirect(f'/movie_details/{movie_id}')
        return redirect(f'/edit_movie_actors/{movie_id}')


class AddMovie(View):

    def get(self, request):
        directors = Director.objects.all()
        actors = Actor.objects.all()
        return render(request, 'add_movie.html', {'directors': directors,
                                                  'actors': actors,
                                                  'ratings': RATING})

    def post(self, request):
        title = request.POST.get('title')
        director = int(request.POST.get('director'))
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        movie = Movie.objects.create(title=title, director_id=director, rating=rating, description=description)
        actors = request.POST.getlist('actors[]')
        for actor in actors:
            ActorMovie.objects.create(actor_id=int(actor), movie_id=movie.id)
        return redirect('/admin_view')


# Login panel view
class Redirect(View):

    def get(self, request):
        if self.request.user.is_superuser:
            return redirect('/admin_view')
        else:
            return redirect('/')
