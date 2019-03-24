from django.conf.urls import include, url
from django.contrib import admin

from search import views as search_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'main.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('users.urls')),
	url(r'^search/', search_views.search, name='search'),
]
