from rest_framework import serializers
from .models import User, Genre, Movie


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    likes_cnt = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', 'release_year', 'genres', 'likes_cnt']

    @staticmethod
    def get_likes_cnt(obj):
        return obj.likes_cnt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Movie
        fields = ['id', 'name', 'release_year', 'genres']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre_name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
            movie.genres.add(genre)
        return movie
