from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movies(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
        


class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 11)])  # Ratings from 1 to 10

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)

    def __str__(self):
        return f"{self.user.username} - {self.movie.name} - {self.rating}"
        
        
        
class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=255)
    date = models.DateField()
    story = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.movie.name}"

class Photo(models.Model):
    image = models.ImageField(upload_to='memories_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    memory = models.ForeignKey(Memory, related_name='photos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo {self.id}"
        
        
