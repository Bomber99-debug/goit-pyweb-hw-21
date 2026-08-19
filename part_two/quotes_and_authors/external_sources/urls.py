from django.urls import path
from . import views

app_name = 'external_sources'

urlpatterns = [
		path('', views.external_sources, name='external_sources'),
		path('mongo_import', views.mongo_import, name='mongo_import'),
		path('scrapi_import', views.scrapi_import, name='scrapi_import'),
		]
