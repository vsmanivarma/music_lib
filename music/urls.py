from django.urls import path
from . import views

urlpatterns = [
    path('', views.music_list, name='music_list'),
    path('register/', views.register_user, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView, name='logout'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('folder/<int:pk>/', views.folder_detail, name='folder_detail'),
    path('select-folder/<int:song_id>/', views.select_folder, name='select_folder'),
    path('update-song/<int:folder_id>/<int:song_id>/', views.update_song, name='update_song'),
    path('delete-song/<int:folder_id>/<int:song_id>/', views.delete_song, name='delete_song'),
    path('upload/', views.upload_song, name='upload_song'),
]
