# Generated by Django 5.0.2 on 2024-03-26 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_movies_budget_movies_director_movies_main_cast_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='director',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='main_cast',
        ),
    ]
