from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import TagForm
from .models import Tag


# Create your views here.
def tags(request, ):
	tags = Tag.objects.all()
	return render(request, 'tags/tags.html', { 'tags': tags })


@login_required
def add_tag(request):
	form = TagForm()
	if request.method == 'POST':
		form = TagForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(to='tags:add_tag')
	return render(request, 'tags/add_tag.html', { 'form': form })
