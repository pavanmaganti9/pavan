from django_elasticsearch_dsl import DocType, Index
from users.models import blog_posts

posts = Index('posts')

@posts.doc_type
class PostDocument(DocType):
	class Meta:
		model = blog_posts
		
		fields = [
			'title',
			'id',
			'tag',
			'author',
		]