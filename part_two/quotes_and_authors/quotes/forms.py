from django.forms import ModelForm, Textarea, Select, CheckboxSelectMultiple
from .models import Quote


class QuoteForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields[ 'author' ].empty_label = None

	class Meta:
		model = Quote
		fields = ('quote', 'author', 'tags')
		widgets = {
				'quote' : Textarea(
						attrs={
								'class': 'form-control',
								'rows' : 5,
								},
						),
				'author': Select(
						attrs={
								'class': 'form-select form-select-lg mb-3',
								'size' : '3',
								},
						),
				'tags'  : CheckboxSelectMultiple(
						attrs={
								'class': 'form-check-input',
								},
						),
				}
