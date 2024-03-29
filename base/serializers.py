from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg
from .models import *
import os


class UserSerializer(serializers.ModelSerializer):

    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isAdmin']
        
    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isAdmin', 'token']
        
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
        
        
        
class MoviesSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = ['id', 'name', 'description', 'average_rating']

    def get_average_rating(self, obj):
        # Calculate the average rating for the movie
        average = MovieRating.objects.filter(movie=obj).aggregate(Avg('rating'))['rating__avg']
        return average if average else 0  # Return 0 if there are no ratings

    def get_description(self, obj):
        # Truncate the description to 100 characters in a meaningful way
        description = obj.description
        if len(description) > 100:
            truncated = description[:100].rsplit(' ', 1)[0]  # Split by the last space within 100 characters
            return f"{truncated} ..."
        return description
        
        
class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ['id', 'movie', 'rating']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        
        
        
class MovieSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'name', 'description'] 
        
        
        
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image', 'uploaded_at']

class MemorySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Memory
        fields = ['id', 'title', 'date', 'story', 'photos', 'movie']
        
class UpdateMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'title', 'story']
        
        
        
class UserMemorySerializer(serializers.ModelSerializer):
    movie_id = serializers.ReadOnlyField(source='movie.id')
    movie_name = serializers.ReadOnlyField(source='movie.name')

    class Meta:
        model = Memory
        fields = ['id', 'movie_id', 'movie_name', 'title']
        
        
 

class PhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.ImageField(source='image')
    photo_name = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    uploaded_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Photo
        fields = ['id', 'photo_url', 'photo_name', 'extension', 'size', 'uploaded_at']

    def get_photo_name(self, obj):
        return os.path.basename(obj.image.name)

    def get_extension(self, obj):
        name, extension = os.path.splitext(obj.image.name)
        return extension.lstrip('.')

    def get_size(self, obj):
        if obj.image and hasattr(obj.image, 'size'):
            size_kb = obj.image.size / 1024  # Convert size to KB
            return f"{round(size_kb, 2)}KB"
        return "Unknown"


class PhotoDetailSerializer(serializers.ModelSerializer):
    photo_name = serializers.SerializerMethodField()
    extension = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    time_created = serializers.DateTimeField(source='uploaded_at', format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Photo
        fields = ['id', 'photo_name', 'extension', 'size', 'time_created']

    def get_photo_name(self, obj):
        return os.path.basename(obj.image.name)

    def get_extension(self, obj):
        name, extension = os.path.splitext(obj.image.name)
        return extension

    def get_size(self, obj):
        if obj.image and hasattr(obj.image, 'size'):
            size_kb = obj.image.size / 1024  # size in KB
            return f"{round(size_kb, 2)}KB"
        return "Unknown"
 
class MemoryDetailSerializer(serializers.ModelSerializer):
    movie_id = serializers.ReadOnlyField(source='movie.id')
    movie_name = serializers.ReadOnlyField(source='movie.name')
    photos = PhotoDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Memory
        fields = ['id', 'movie_id', 'movie_name', 'title', 'story', 'photos']
        
        
