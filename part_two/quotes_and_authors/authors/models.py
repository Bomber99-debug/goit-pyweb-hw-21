from django.db import models

# Create your models here.
class Author(models.Model):
	fullname = models.CharField(max_length=150)
	born_date = models.DateField()
	born_location = models.CharField(max_length=200)
	description = models.TextField()

	def __str__(self):
		return self.fullname