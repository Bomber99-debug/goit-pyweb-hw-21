from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MongoDBImportForm
from .services import import_data
from .scraping_site import scrapi_data


# Create your views here.
@login_required
def external_sources(request):
	return render(request, 'external_sources/external_sources.html')


@login_required
def mongo_import(request):
	form = MongoDBImportForm()
	if request.method == 'POST':
		form = MongoDBImportForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			import_data(data)
			messages.success(request, 'Дані успішно імпортовано')
	return render(request, 'external_sources/mongo_import.html', { 'form': form })

@login_required
def scrapi_import(request):
	len_tags, len_author, len_quotes = scrapi_data()
	return render(request, 'external_sources/external_sources.html', {
			'len_tags': len_tags,
			'len_author': len_author,
			'len_quotes': len_quotes,
			})