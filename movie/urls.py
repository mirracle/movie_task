from django.urls import path

from movie.views import UserCreateView, MovieCreateView, MovieListView, MovieLikeView

urlpatterns = [
    path('user/', UserCreateView.as_view()),
    path('film/', MovieCreateView.as_view()),
    path('film/list/', MovieListView.as_view()),
    path('film/<int:pk>/like/<int:user_id>/', MovieLikeView.as_view()),
]
