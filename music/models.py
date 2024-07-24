from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to='music/')

    def __str__(self):
        return self.title

class Folder(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    music_tracks = models.ManyToManyField(Music, blank=True, related_name='folders')

    def __str__(self):
        return self.name

# Signal to create default "Favorites" folder
@receiver(post_save, sender=User)
def create_default_favorites_folder(sender, instance, created, **kwargs):
    if created:
        if not Folder.objects.filter(owner=instance, name='Favorites').exists():
            Folder.objects.create(name='Favorites', owner=instance)
