from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import Parameter, IN_HEADER, IN_QUERY, TYPE_STRING, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, filters
from rest_framework.response import Response

from movie.filters import MovieFilter
from movie.models import Movie, User
from movie.serializers import MovieListSerializer, UserSerializer, MovieCreateSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.annotate(likes_cnt=Count('likes')).order_by('name')
    serializer_class = MovieListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = MovieFilter

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genres__name__icontains=genre)
        most_liked = self.request.query_params.get('most_liked', None)
        if most_liked:
            queryset = queryset.order_by('-likes_cnt')
        return queryset


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieCreateView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer


class MovieLikeView(generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer

    def post(self, request, *args, **kwargs):
        movie = self.get_object()
        user_id = kwargs.get('user_id')
        user = User.objects.get(pk=user_id)
        movie.likes.add(user)
        movie.save()
        return Response({'status': 'success'})
