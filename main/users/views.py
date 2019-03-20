from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import PostForm, UploadFileForm
from .models import blog_posts, Document
from django.core.files.storage import FileSystemStorage


def index(request):
	return render(request, 'index.html', {'title' : 'Home'})

def register(request):
	if request.method == 'POST':
		form  = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			form.save()
			messages.success(request, 'Account Created')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'register.html', {'form':form, 'title' : 'Register'})
	
def login(request):
	return render(request, 'login.html', {'title' : 'Login'})
	
def logout(request):
	#return redirect('login')
	return render(request, 'logout.html', {'title' : 'Logout'})
	
@login_required(login_url='/login/')
def profile(request):
	return render(request, 'profile.html', {'title' : 'Profile'})
	
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('data')
    return render(request, 'post_form.html', {'form': form})
	
def data(request):
	Website = blog_posts.objects.all()
	page = request.GET.get('page', 1)
	paginator = Paginator(Website, 3)
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
		# context = {
		# 'title' : 'Dynamic',
		# 'website' : Website,
		# 'users': users
	# }
	return render(request, 'data.html', { 'users': users,'title' : 'Dynamic Content' })
	
def details(request, id):
	Content = blog_posts.objects.get(id=id)
	context = {
		'content' : Content,
		'title' : 'Content Details'
	}
	return render(request, 'details.html', context)
	
def update(request, pk):
    post = get_object_or_404(blog_posts, pk=pk)
    form = blog_posts.objects.get(id=pk)
    return render(request, 'edit.html', {'form': form})
	
def edit(request,pk):
	forme = get_object_or_404(blog_posts, id=pk)
	form = PostForm(request.POST or None, instance=forme)
	if form.is_valid():
		form.save()
        return redirect('data')
		
def delete(request,pk):
	forme = get_object_or_404(blog_posts, id=pk)
	if 'POST' == request.method:
		forme.delete()
		return redirect('data')
	return render(request, 'delete.html', {'object':forme,'title' : 'Delete Content'})
	
def passwordreset(request):
	return render(request, 'password_reset.html', {'title' : 'Dynamic Content'})
	
def file_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html', {'title' : 'File Upload'})
	