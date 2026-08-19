from django.db import models
from authors.models import Author
from tags.models import Tag


# Create your models here.
class Quote(models.Model):
	quote = models.TextField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, related_name='quotes')

	def __str__(self):
		return self.quote
