from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Document

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		
from .models import blog_posts

class PostForm(forms.ModelForm):

    class Meta:
        model = blog_posts
        fields = ('title', 'tag', 'author')
		
class UploadFileForm(forms.Form):
    class Meta:
        model = Document
        fields = ['description', 'document', ]