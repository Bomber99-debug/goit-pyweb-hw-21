import re
import requests
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Generator
from bs4 import BeautifulSoup
from datetime import datetime

from authors.models import Author
from quotes.models import Quote
from tags.models import Tag


def get_page_soup(url: str) -> BeautifulSoup:
	response = requests.get(url, timeout=5)
	response.raise_for_status()

	soup = BeautifulSoup(response.content, 'lxml')

	return soup


def extract_quotes_data(
		soup: BeautifulSoup,
		) -> Generator[ dict[ str, str | list[ str ] ], None, None ]:
	quote_blocks = soup.find_all('div', class_='quote')

	for quote_block in quote_blocks:
		quote_element = quote_block.find('span', class_="text")
		author_element = quote_block.find('small', class_='author')
		tag_container = quote_block.find('div', class_='tags')

		tag_elements = tag_container.find_all('a', class_='tag')

		quote_data = {
				'quote' : quote_element.text if quote_element else None,
				'author': author_element.text if author_element else None,
				'tags'  : [ tag.text for tag in tag_elements ] if tag_elements else [ ],
				}

		yield quote_data


def create_tag(tag: str) -> tuple[ str, Tag ]:
	obj, created = Tag.objects.get_or_create(
			name=tag,
			)

	return tag, obj


def extract_author_urls(
		base_url: str,
		soup: BeautifulSoup,
		visited_author_paths: set[ str ],
		) -> list[ str ]:
	quote_blocks = soup.find_all('div', class_='quote')

	author_urls = [ ]

	for quote_block in quote_blocks:
		author_link = quote_block.find('a')

		if author_link is None:
			continue

		author_path = author_link.get('href')

		if author_path is None:
			continue

		if author_path in visited_author_paths:
			continue

		visited_author_paths.add(author_path)

		author_url = base_url + author_path
		author_urls.append(author_url)

	return author_urls


def extract_author_data(author_url: str) -> dict[ str, str ]:
	author_soup = get_page_soup(author_url)

	fullname_element = author_soup.find('h3', class_='author-title')
	born_date_element = author_soup.find('span', class_='author-born-date')
	if born_date_element:
		date_obj = datetime.strptime(born_date_element.text, '%B %d, %Y')
		born_date_element = date_obj.strftime('%Y-%m-%d')
	else:
		born_date_element = None

	born_location_element = author_soup.find('span', class_='author-born-location')
	description_element = author_soup.find('div', class_='author-description')
	author_data = {
			'fullname'     : fullname_element.text if fullname_element else None,
			'born_date'    : born_date_element,
			'born_location': born_location_element.text if born_location_element else None,
			'description'  : description_element.text.strip() if description_element else None,
			}

	return author_data


def create_author(author_data: dict[ str, str ]) -> tuple[ str, Author ]:
	obj, created = Author.objects.get_or_create(
			fullname=author_data[ 'fullname' ],
			born_date=author_data[ 'born_date' ],
			defaults={
					'born_location': author_data[ 'born_location' ],
					'description'  : author_data[ 'description' ],
					},
			)
	return (author_data[ 'fullname' ], obj)


def get_next_page_path(soup: BeautifulSoup) -> str | None:
	next_page_element = soup.find('li', class_='next')

	if next_page_element is None:
		return None

	next_page_link = next_page_element.find('a')

	if next_page_link is None:
		return None

	return next_page_link.get('href')


def scrapi_data() -> tuple[ int, int, int ]:
	base_url = 'https://quotes.toscrape.com'
	next_page_path = '/'
	page_number = '1'

	visited_author_paths: set[ str ] = set()

	all_quotes = [ ]
	authors_map = { }
	tags = set()
	tags_map = { }

	author_futures = [ ]
	with ThreadPoolExecutor(max_workers=5) as executor:
		while next_page_path is not None:
			page_url = base_url + next_page_path
			soup = get_page_soup(page_url)

			print(f'Scrape page: {page_number}')
			for author_url in extract_author_urls(base_url, soup, visited_author_paths):
				author_futures.append(
						executor.submit(extract_author_data, author_url),
						)

			for quote_data in extract_quotes_data(soup):
				for tag in quote_data[ 'tags' ]:
					tags.add(tag)
				all_quotes.append(quote_data)

			next_page_path = get_next_page_path(soup)

			if next_page_path is not None:
				page_number = re.search(r"\d+", next_page_path).group()

		for tag in tags:
			k, v = create_tag(tag)
			tags_map[ k ] = v

		for author_future in author_futures:
			try:
				item = create_author(author_future.result())
				k, v = item
				authors_map[ k ] = v
			except Exception as error:
				print(f'Error while processing author: {error}')
				continue

		for quote_data in all_quotes:
			if quote_data[ 'author' ] in authors_map:
				obj, created = Quote.objects.get_or_create(
						quote=quote_data[ 'quote' ],
						author=authors_map[ quote_data[ 'author' ] ],
						)
				tags = set()
				for tag in quote_data[ 'tags' ]:
					tags.add(tags_map[ tag ])
				obj.tags.set(tags)
			else:
				continue

		len_tags = len(tags_map)
		len_author = len(authors_map)
		len_quotes = len(all_quotes)
		return len_tags, len_author, len_quotes
