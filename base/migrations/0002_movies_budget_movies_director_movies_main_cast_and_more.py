# Generated by Django 5.0.2 on 2024-03-25 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='budget',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='movies',
            name='director',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='movies',
            name='main_cast',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movies',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='movies',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='movies',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
