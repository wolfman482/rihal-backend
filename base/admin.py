from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Movies)
admin.site.register(MovieRating)
admin.site.register(Memory)
admin.site.register(Photo)