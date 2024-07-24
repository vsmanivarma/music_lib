from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Music,Folder

class RegistrationForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email','password1','password2']

class MusicForm(forms.ModelForm):
    folders = forms.ModelMultipleChoiceField(queryset=Folder.objects.none(), required=False)

    class Meta:
        model = Music
        fields = ['title', 'artist', 'genre', 'language','file_upload',]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['folders'].queryset = Folder.objects.filter(owner=user)

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']