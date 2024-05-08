from django.db import OperationalError
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.response import Response

from movie.filters import MovieFilter
from movie.models import Movie, User
from movie.serializers import MovieListSerializer, UserSerializer, MovieCreateSerializer
from movies_project.pagination import MediumPagination


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.annotate(likes_cnt=Count('likes')).order_by('name')
    serializer_class = MovieListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = MovieFilter
    pagination_class = MediumPagination

    def filter_queryset(self, queryset):
        return queryset

    def get_queryset(self):
        try:
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
        except OperationalError:
            return Response(
                {'status': 'error', 'message': 'Ошибка обработки запроса'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        try:
            movie_id = kwargs.get('pk')
            movie = Movie.objects.get(pk=movie_id)
            user_id = kwargs.get('user_id')
            user = User.objects.get(pk=user_id)
        except Movie.DoesNotExist:
            return Response(
                {'status': 'fail', 'message': 'Фильм не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'status': 'fail', 'message': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        movie.likes.add(user)
        movie.save()
        return Response({'status': 'success'})
