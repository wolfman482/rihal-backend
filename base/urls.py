from django.urls import path
from . import views


urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('movies/', views.getMovies, name="movies"),
    path('movie/<int:movie_id>/', views.get_movie_details, name="movie"),
    path('rate-movie/', views.rate_movie, name="rate-movie"),
    path('guess-movie/<str:scrambled_name>/', views.guess_movie, name='guess-movie'),

    path('compare-ratings/', views.compare_ratings, name='compare-ratings'),
    
    
    path('memories/add/', views.add_memory_with_photos, name='add-memory'),
    path('memories/', views.get_my_memories, name='my-memories'),
    path('memories/<int:memory_id>/', views.get_memory_detail, name='memory-detail'),
    path('memories/update/<int:memory_id>/', views.update_memory, name='update-memory'),
    
    
    path('photos/<int:photo_id>/', views.get_photo_detail, name='photo-detail'),
    path('memories/<int:memory_id>/upload-photos/', views.upload_photos_to_memory, name='upload-photos-to-memory'),
    path('memories/<int:memory_id>/delete-photos/', views.delete_photos_from_memory, name='delete-photos-from-memory'),
    path('memories/delete/<int:memory_id>/', views.delete_memory, name='delete-memory'),
    path('memories/<int:memory_id>/extract-urls/', views.extract_urls_from_memory, name='extract-urls'),
    path('memories/top-words/', views.top_words_in_memories, name='top-words-in-memories'),



    
    path('my-top-rated/', views.my_top_rated_movies, name="my-top-rated-movies"),
    path('search/', views.search_movies, name="search-movies"),
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    
    path('register/', views.registerUser, name="register"),
    
    
    path('min-stars/', views.get_min_stars_for_movies, name='get-min-stars-for-movies'),
]