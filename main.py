from pprint import pprint
import bs4
import requests
import json
from fake_headers import Headers


all_pages_data = []
links = []
search_results = []


def get_headers():
	return Headers(os="win", browser="Chrome").generate()


def get_all_data():
	link = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page="
	pages = 1
	for page in range(pages):
		link_for_page = f'{link}{page}'
		response = requests.get(link_for_page, headers=get_headers())
		if response.status_code == 200:
			main_html_data = response.text
			main_soup = bs4.BeautifulSoup(main_html_data, features="lxml")
			tag_div_article_list = main_soup.find("div", attrs={"data-qa": "vacancy-serp__results"})
			all_pages_data.append(tag_div_article_list)
		else:
			print(response.status_code)
			break
	return all_pages_data


def search_key_words():
	keywords = ["Django", "Flask"]
	for page_data in all_pages_data:
		tag_div_article_list = page_data.find_all("h2", attrs={"data-qa": "bloko-header-2"})
		for tag in tag_div_article_list:
			article_tag = tag.find("a", class_="bloko-link", href=True)
			links.append(article_tag["href"])
	for link in links:
		response = requests.get(link, headers=get_headers())
		if response.status_code == 200:
			main_html_data = response.text
			main_soup = bs4.BeautifulSoup(main_html_data, features="lxml")
			tag_div_article_list = main_soup.find("div", attrs={"data-qa": "vacancy-description"})
			for keyword in keywords:
				try:
					if keyword in tag_div_article_list.text:
						search_results.append(link)
				except AttributeError:
					continue
		else:
			print(response.status_code)
	return search_results


if __name__ == '__main__':
	get_all_data()
	# print(all_pages_data)
	search_key_words()
	pprint(links)
	pprint(search_results)
