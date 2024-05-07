from django_filters import rest_framework as filters

from movie.models import Movie


class MovieFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name="genres__name__icontains")
    most_liked = filters.NumberFilter(field_name="likes_count")
