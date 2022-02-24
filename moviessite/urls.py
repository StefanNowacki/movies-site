"""moviessite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from moviessite_app.views import Movies, MovieDetails, AdminView, DeleteMovie, EditMovie, AddMovie, EditMovieActors, DeleteMovieActors, Redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Movies.as_view()),
    path('movie_details/<int:movie_id>', MovieDetails.as_view(), name='movie-details'),
    path('admin_view', AdminView.as_view()),
    path('delete_movie/<int:movie_id>', DeleteMovie.as_view()),
    path('edit_movie/<int:movie_id>', EditMovie.as_view()),
    path('add_movie', AddMovie.as_view()),
    path('edit_movie_actors/<int:movie_id>', EditMovieActors.as_view()),
    path('delete_actor/<int:movie_actor_id>', DeleteMovieActors.as_view()),
    path('redirect', Redirect.as_view())
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
