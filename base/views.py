import requests
import humanize
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.db.models import Q

from django.http import JsonResponse
from .movies import movies
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

# Create your views here.


url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
nltk.download('stopwords')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        serializer = UserSerializerWithToken(self.user).data
        
        for k, v in serializer.items():
            data[k] = v
        
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



def calculate_min_stars(ratings):
    n = len(ratings)
    stars = [1] * n
    
    # Left to right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            stars[i] = stars[i - 1] + 1
            
    # Right to left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            stars[i] = max(stars[i], stars[i + 1] + 1)
    
    return sum(stars)


   
@api_view(['POST'])
def registerUser(request):
    data = request.data
    
    try:
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


def getRoutes(request):
    return JsonResponse('hello', safe=False)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMovies(request):
    movies = Movies.objects.all()
    serializer = MoviesSerializer(movies, many=True)
    return Response(serializer.data)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie_details(request, movie_id):
    try:
        movie = Movies.objects.get(id=movie_id)
        serializer = MoviesSerializer(movie)
        movie_data = serializer.data

        # Fetch additional details from the external API
        external_api_url = f'https://cinema.stag.rihal.tech/api/movie/{movie_id}'
        response = requests.get(external_api_url)
        if response.status_code == 200:
            external_data = response.json()
            movie_data.update({
                'release_date': external_data.get('release_date'),
                'main_cast': external_data.get('main_cast'),
                'director': external_data.get('director'),
                'budget': external_data.get('budget'),
                'budget_in_words': humanize.intword(external_data.get('budget', 0))
            })

        average_rating = MovieRating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg'] or 0
        movie_data['average_rating'] = average_rating

        user_rating = MovieRating.objects.filter(movie=movie, user=request.user).first()
        movie_data['my_rating'] = user_rating.rating if user_rating else None

        return Response(movie_data)
    except Movies.DoesNotExist:
        return Response({'detail': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_movie(request):
    serializer = MovieRatingSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies(request):
    query = request.query_params.get('q', '')
    movies = Movies.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    serializer = MovieSearchSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_top_rated_movies(request):
    user_ratings = MovieRating.objects.filter(user=request.user).order_by('-rating')[:5]
    movies = [rating.movie for rating in user_ratings]
    data = [{
        'id': movie.id,
        'name': movie.name,
        'rating': next((rating.rating for rating in user_ratings if rating.movie_id == movie.id), None)
    } for movie in movies]
    return Response(data)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def add_memory_with_photos(request):
    movie_id = request.data.get('movie')
    
    if not movie_id:
        return JsonResponse({'error': 'movie is required'}, status=400)

    movie = get_object_or_404(Movies, id=movie_id)
    memory = Memory.objects.create(
        user=request.user,
        movie=movie,
        title=request.data.get('title'),
        date=request.data.get('date'),
        story=request.data.get('story')
    )
    
    photos = request.FILES.getlist('photos')
    for photo in photos:
        Photo.objects.create(image=photo, memory=memory)

    serializer = MemorySerializer(memory)
    return Response(serializer.data)

    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_memories(request):
    memories = Memory.objects.filter(user=request.user)
    serializer = UserMemorySerializer(memories, many=True)
    return Response(serializer.data)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_memory_detail(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    serializer = MemoryDetailSerializer(memory)
    return Response(serializer.data)
    

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, memory__user=request.user)
    serializer = PhotoSerializer(photo)
    return Response(serializer.data)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_photos_to_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    photos = request.FILES.getlist('photos')  # 'photos' is the key in the multipart/form-data request

    for photo in photos:
        Photo.objects.create(image=photo, memory=memory)

    return Response({'message': 'Photos uploaded successfully.'}, status=status.HTTP_201_CREATED)
    
  

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_photos_from_memory(request, memory_id):
    get_object_or_404(Memory, id=memory_id, user=request.user)
    
    photo_ids = request.data.get('photo_ids', [])
    
    if not photo_ids:
        return Response({'message': 'No photo IDs provided.'}, status=status.HTTP_400_BAD_REQUEST)


    Photo.objects.filter(memory_id=memory_id, id__in=photo_ids).delete()

    return Response({'message': 'Photos deleted successfully.'})
  
 


 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    serializer = UpdateMemorySerializer(memory, data=request.data, partial=True) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    memory.delete()
    return Response({'message': 'Memory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def extract_urls_from_memory(request, memory_id):
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    story = memory.story

    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', story)
    return Response({'urls': urls})
    
    
    
@api_view(['GET'])
@permission_classes([AllowAny])
def top_words_in_memories(request):
    stories = Memory.objects.all().values_list('story', flat=True)
    text = ' '.join(stories)
    
    words = re.findall(r'\b\w+\b', text.lower())
    
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    
    word_counts = Counter(filtered_words).most_common(5)
    
    top_words = [{'word': word, 'count': count} for word, count in word_counts]
    return Response({'top_words': top_words})
    
    
@api_view(['GET'])
def guess_movie(request, scrambled_name):
    normalized_input = ''.join(sorted(scrambled_name.lower()))
    
    for movie in Movies.objects.all():
        normalized_movie_name = ''.join(sorted(movie.name.lower()))
        if normalized_input == normalized_movie_name:
            serializer = MoviesSerializer(movie)
            return Response(serializer.data)
    
    
    return Response({"message": "404 not found"}, status=404)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def compare_ratings(request):
    user_ratings = MovieRating.objects.filter(user=request.user).select_related('movie')
    movie_ids = user_ratings.values_list('movie', flat=True)
    average_ratings = (MovieRating.objects.filter(movie__in=movie_ids)
                       .values('movie')
                       .annotate(average_rating=Avg('rating'))
                       .order_by())

    comparison_list = []

    for user_rating in user_ratings:
        movie_id = user_rating.movie.id
        movie_name = user_rating.movie.name
        average_rating = next((item for item in average_ratings if item['movie'] == movie_id), None)

        if average_rating and user_rating.rating >= average_rating['average_rating']:
            comparison_list.append({'id': movie_id, 'name': movie_name, 'rating': user_rating.rating, 'is_user_rating': True})
        elif average_rating:
            comparison_list.append({'id': movie_id, 'name': movie_name, 'rating': average_rating['average_rating'], 'is_user_rating': False})

    return Response(comparison_list)
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_min_stars_for_movies(request):
    movie_ids = request.data.get('movie_ids', [])
    
    if not movie_ids:
        return Response({"error": "No movie IDs provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    movies_with_ratings = (MovieRating.objects.filter(movie_id__in=movie_ids)
                           .values('movie_id')
                           .annotate(average_rating=Avg('rating'))
                           .order_by())

    ratings_dict = {rating['movie_id']: rating['average_rating'] for rating in movies_with_ratings}

    ordered_ratings = [ratings_dict.get(movie_id, 0) for movie_id in movie_ids]
    
    min_stars = calculate_min_stars(ordered_ratings)
    return Response({'min_stars': min_stars})