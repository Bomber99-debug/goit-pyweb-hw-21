from django.forms import ModelForm, CharField, DateField, DateInput, TextInput, Textarea
from .models import Author


class AuthorForm(ModelForm):
	fullname = CharField(
			min_length=3,
			max_length=150,
			required=True,
			widget=TextInput(
					attrs={
							'class'      : 'form-control form-label',
							'placeholder': 'Повне ім\'я автора',
							'type'       : 'text',
							},
					),

			)
	born_date = DateField(
			widget=DateInput(
					attrs={
							'class': 'form-control',
							'type' : 'date',
							},
					format='%Y-%m-%d',
					),
			)
	born_location = CharField(
			min_length=10,
			max_length=150,
			required=True,
			widget=TextInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'Місце народження автора',
							'type'       : 'text',
							},
					),
			)
	description = CharField(
			min_length=30,
			widget=Textarea(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'Коротка біографія автора',
							'rows'       : '10',
							'cols'       : '100',
							},
					),
			)

	class Meta:
		model = Author
		fields = [ 'fullname', 'born_date', 'born_location', 'description' ]
