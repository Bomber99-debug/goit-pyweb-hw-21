from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author
from .forms import AuthorForm


# Create your views here.
def authors(request):
	authors = Author.objects.all()
	paginator = Paginator(authors, 18)
	page = request.GET.get('page')
	authors = paginator.get_page(page)
	return render(request, 'authors/authors.html', context={ 'authors': authors })

def author(request, author_id):
	author = get_object_or_404(Author, id=author_id)
	return render(request, 'authors/author.html', { 'author': author})


@login_required
def add_author(request):
	form = AuthorForm()
	if request.method == 'POST':
		form = AuthorForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(to='authors:add_author')
	return render(request, 'authors/add_author.html', context={ 'form': form })
