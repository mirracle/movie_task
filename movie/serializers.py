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

    @staticmethod
    def validate_release_year(value):
        if value > 9999 or value < 1900:
            raise serializers.ValidationError(
                "Введен неправильный формат даты выпуска. Доступные значения от 1900 до 9999"
            )
        return value

    @staticmethod
    def validate_genres(value):
        if not value:
            raise serializers.ValidationError(
                "Вы не указали жанры фильма"
            )

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        genrs = [Genre(name=genre_name.strip()) for genre_name in genres_data]
        Genre.objects.bulk_create(genrs)
        movie.genres.set(genrs)
        return movie
