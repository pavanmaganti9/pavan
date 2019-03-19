from django.conf.urls import url,include
from django.contrib import admin
from .import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/', views.register, name='register'),
	url(r'^login/', auth_views.login, name='login'),
	# url(r'^signup/$', views.signup, name='signup'),
	# url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^new/$', views.post_create, name='post_create'),
	url(r'^data/$', views.data, name='data'),
	url(r'^details/(?P<id>\d+)/$', views.details, name='details'),
	url(r'^update/(?P<pk>\d+)$', views.update, name='update'),
	url(r'^edit/(?P<pk>\d+)/$', views.edit, name='edit'),
	url(r'^delete/(?P<pk>\d+)/$', views.delete, name='delete'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
