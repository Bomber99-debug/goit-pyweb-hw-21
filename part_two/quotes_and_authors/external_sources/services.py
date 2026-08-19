from pymongo import MongoClient
from pymongo.server_api import ServerApi

from datetime import datetime

from authors.models import Author
from quotes.models import Quote
from tags.models import Tag


def import_data(data: dict):
	username = data[ 'username' ]
	password = data[ 'password' ]
	db_name = data[ 'db_name' ]
	host = data[ 'host' ]
	app_name = data[ 'app_name' ]

	client = MongoClient(
			f'mongodb+srv://{username}:{password}@{host}/?appName={app_name}',
			server_api=ServerApi('1'),
			)

	authors_map = { }
	tags_map = { }

	db = client[ db_name ]
	authors_mongodb = db[ 'author' ]

	for author in authors_mongodb.find():
		date_obj = datetime.strptime(author[ 'born_date' ], '%B %d, %Y')
		object_born_date = date_obj.strftime('%Y-%m-%d')

		obj, created = Author.objects.get_or_create(
				fullname=author[ 'fullname' ],
				born_date=object_born_date,
				defaults={
						'born_location': author[ 'born_location' ],
						'description'  : author[ 'description' ],
						},
				)

		authors_map[ author[ '_id' ] ] = obj

	quotes_mongodb = db[ 'quote' ]
	for quote in quotes_mongodb.find():
		for tag in quote[ 'tags' ]:
			obj, created = Tag.objects.get_or_create(
					name=tag,
					)
			tags_map[ tag ] = obj

		obj, created = Quote.objects.get_or_create(
				quote=quote[ 'quote' ],
				author=authors_map[ quote[ 'author' ] ],
				)
		tags = set()
		for tag in quote[ 'tags' ]:
			tags.add(tags_map[ tag ])
		obj.tags.set(tags)
