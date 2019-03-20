from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class blog_posts(models.Model):
    title = models.CharField(max_length=400)
    tag = models.CharField(max_length=50)
    author = models.CharField(max_length=120)
		
    def __unicode__(self):
        return self.title

    def get_post_url(self):
        return reverse('post_edit', kwargs={'pk': self.pk})
		
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	
	def __str__(self):
		return self.user.username