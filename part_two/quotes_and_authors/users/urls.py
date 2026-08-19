from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
		path('logout/', LogoutView.as_view(), name='logout'),
		path('register/', views.RegisterView.as_view(), name='register'),
		path(
				'login/',
				LoginView.as_view(
						template_name='users/login.html',
						form_class=LoginForm,
						redirect_authenticated_user=True,
						),
				name='login',
				),
		]
