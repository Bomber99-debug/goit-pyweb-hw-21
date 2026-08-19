from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import QuoteForm
from .models import Quote
from tags.models import Tag


# Create your views here.
def index(request):
	quotes = Quote.objects.all()

	paginator = Paginator(quotes, 5)
	page = request.GET.get('page')
	quotes = paginator.get_page(page)

	top_ten_tags = Tag.objects.annotate(quote_count=Count('quotes')).order_by('-quote_count')[ :10 ]
	return render(
			request,
			'quotes/index.html',
			{
					'quotes'      : quotes,
					'top_ten_tags': top_ten_tags,
					},
			)


def quotes_tags(request, quotes_tag_id):
	tags = get_object_or_404(Tag, id=quotes_tag_id)
	quotes = tags.quotes.all()
	paginator = Paginator(quotes, 5)
	page = request.GET.get('page')
	quotes = paginator.get_page(page)

	top_ten_tags = Tag.objects.annotate(quote_count=Count('quotes')).order_by('-quote_count')[ :10 ]
	return render(
			request,
			'quotes/index.html',
			{
					'tags'        : tags,
					'quotes'      : quotes,
					'top_ten_tags': top_ten_tags,
					},
			)


@login_required
def add_quote(request):
	form = QuoteForm()
	if request.method == 'POST':
		form = QuoteForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(to='quotes:add_quote')
	return render(request, 'quotes/add_quote.html', { 'form': form })
