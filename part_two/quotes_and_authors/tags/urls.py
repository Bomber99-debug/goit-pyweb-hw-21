from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
		path('', views.tags, name='tags'),
		path('add_tag/', views.add_tag, name='add_tag'),
		]