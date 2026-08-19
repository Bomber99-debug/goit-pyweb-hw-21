from django.forms import Form, CharField, TextInput, PasswordInput


class MongoDBImportForm(Form):
	username = CharField(
			label="Username",
			required=True,
			widget=TextInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'MongoDB username, e.g. my_user',
							},
					),
			)

	password = CharField(
			label="Password",
			required=True,
			widget=PasswordInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'MongoDB password',
							},
					),
			)

	db_name = CharField(
			label="Database Name",
			required=True,
			widget=TextInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'Database name, e.g. hw',
							},
					),
			)

	host = CharField(
			label="Database Host",
			required=True,
			widget=TextInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'Cluster host, e.g. cluster0.xxxxx.mongodb.net',
							},
					),
			)

	app_name = CharField(
			label="Application Name",
			required=True,
			initial="Cluster0",
			widget=TextInput(
					attrs={
							'class'      : 'form-control',
							'placeholder': 'Application name, e.g. Cluster0',
							},
					),
			)
	# collection_name = CharField(
	# 		label="Collection Name",
	# 		required=False,
	# 		widget=TextInput(
	# 				attrs={
	# 						'class'      : 'form-control',
	# 						'placeholder': 'Optional. Leave empty to use default collections: authors, quotes',
	# 						},
	# 				),
	# 		)
