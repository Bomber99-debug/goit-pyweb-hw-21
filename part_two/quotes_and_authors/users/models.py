from django.db import models


# Create your models here.
class Profile( models.Model ):
	avatar = models.TextField()

	def __str__( self ):
		return self.avatar
