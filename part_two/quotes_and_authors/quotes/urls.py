from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
		path('', views.index, name='home'),
		path('tags/<int:quotes_tag_id>/', views.quotes_tags, name='quotes_tags'),
		path('quotes/add_quote/', views.add_quote, name='add_quote'),
		]