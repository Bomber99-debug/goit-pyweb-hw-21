from django.forms import ModelForm, CharField, TextInput

from .models import Tag


class TagForm(ModelForm):
	name = CharField(
			min_length=1,
			max_length=100,
			required=True,
			widget=TextInput(
					attrs={
							'class': 'form-control',
							'type' : 'text',
							},
					),
			)

	class Meta:
		model = Tag
		fields = ('name',)