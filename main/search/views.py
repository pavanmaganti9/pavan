from django.shortcuts import render
from search.documents import PostDocument
# Create your views here.

def search(request):
	q = request.GET.get('q')
	if q:
		posts = PostDocument.search().query("match", title=q)
	else:
		posts = ''
		
	return render(request, 'search.html', {'posts':posts,'title':'Elastic Search'})