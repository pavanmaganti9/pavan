from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm

def register(request):
	if request.method == 'POST':
		form  = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			form.save()
			messages.success(request, 'Account Created')
			return redirect('register')
	else:
		form = UserRegistrationForm()
	return render(request, 'register.html', {'form':form})