from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Music, Folder
from .forms import RegistrationForm, FolderForm,MusicForm

def music_list(request):
    songs = Music.objects.all()
    favorites_folder = None
    folders = []
    if request.user.is_authenticated:
        favorites_folder = Folder.objects.filter(owner=request.user, name='Favorites').first()
        folders = Folder.objects.filter(owner=request.user).exclude(name='Favorites')

    return render(request, 'list.html', {
        'songs': songs,
        'favorites_folder': favorites_folder,
        'folders': folders
    })

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('music_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('music_list')

def CustomLogoutView(request):
    return render(request, 'thanks.html')

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            return redirect('music_list')
    else:
        form = FolderForm()
    return render(request, 'create_folder.html', {'form': form})

@login_required
def folder_detail(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    return render(request, 'folder_detail.html', {'folder': folder})

@login_required
def select_folder(request, song_id):
    song = get_object_or_404(Music, id=song_id)
    folders = Folder.objects.filter(owner=request.user)
    if request.method == 'POST':
        folder_id = request.POST.get('folder')
        folder = get_object_or_404(Folder, id=folder_id)
        folder.music_tracks.add(song)
        return redirect('folder_detail', pk=folder_id)
    return render(request, 'select_folder.html', {'song': song, 'folders': folders})


@login_required
def update_song(request, folder_id, song_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    current_song = get_object_or_404(Music, pk=song_id)
    all_songs = Music.objects.exclude(id=current_song.id)  

    if request.method == 'POST':
        new_song_id = request.POST.get('new_song')
        new_song = get_object_or_404(Music, pk=new_song_id)

        # Update the folder with the new song
        folder.music_tracks.remove(current_song)
        folder.music_tracks.add(new_song)

        return redirect('folder_detail', pk=folder_id)

    return render(request, 'update_song.html', {
        'folder': folder,
        'current_song': current_song,
        'all_songs': all_songs,
    })

@login_required
def delete_song(request, folder_id, song_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    song = get_object_or_404(Music, id=song_id)
    if request.method == 'POST':
        folder.music_tracks.remove(song)
        return redirect('folder_detail', pk=folder_id)
    return render(request, 'delete_song.html', {'folder': folder, 'song': song})


def upload_song(request):
    if request.method == 'POST':
        form = MusicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('music_list')  
    else:
        form = MusicForm()

    return render(request, 'upload_song.html', {'form': form})
