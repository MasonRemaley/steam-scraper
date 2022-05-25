####
### Scraping implementation.
####

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

import date

from tags import TAG_IDS
from tags import TAG_NAMES

def scrape(tags, start, end):
	# Convert the args
	start = date.start(start)
	end = date.end(end)
	if type(tags) != list:
		tags = [tags]
	try:
		tags = "%2C".join([str(TAG_IDS[tag]) for tag in tags])
	except KeyError as tag:
		print(f"Error: tag {tag} not found in 'tags.py'")
		return None

	# The output data
	output = {}

	# Scrape on page at a time starting from the present until we pass the start date
	current_date = end
	result_index = 0
	while current_date > start:
		# Build the URL
		max_results = 25 # The minimum that's respected
		url = ("https://store.steampowered.com/search/?sort_by=Released_DESC&tags=" +
			f"{tags}&category1=998&category3=2&os=win&start={result_index}&count={max_results}")

		# Make the request
		print(f"Scraping `{url}`, CTRL+C to cancel...")
		headers = {"Accept-Language": "en-US, en;q=0.5"}
		results = requests.get(url, headers=headers)

		# Parse the results and increment our result counter
		soup = BeautifulSoup(results.text, "html.parser")
		scraped_games = soup.find_all("a", class_="search_result_row")
		result_index += len(scraped_games)

		# Process each game
		for game in scraped_games:
			store_page = "/".join(game["href"].split("/")[0:-1])

			title = game.find("span", class_="title").text

			release_date = game.find("div", class_="search_released")
			if release_date:
				release_date = release_date.text.strip()
				try:
					release_date = datetime.strptime(release_date, "%b %d, %Y").date()
					current_date = release_date
				except ValueError:
					release_date = None

			reviews = game.find("span", class_="search_review_summary")
			if reviews:
				reviews = reviews["data-tooltip-html"]
				reviews = reviews.replace(",", "")
				reviews = int(re.search(r"(\d+) user reviews", reviews)[1])
			else:
				reviews = 0

			price = game.find("div", class_="search_price")
			if price and price.text.strip() != "":
				if price.text.strip() == "Free To Play":
					price = 0.0
				else:
					price = re.search(r"\$(\d+\.\d\d)", price.text)
					if price:
						price = float(price[1])
			else:
				price = None

			top_tags = [TAG_NAMES[int(tag)] for tag in game["data-ds-tagids"][1:-1].split(",")]

			if release_date and (start <= release_date <= end):
				output[title] = {
					"title": title,
					"store_page": store_page,
					"release_date": date.format_optional(release_date),
					"reviews": reviews,
					"price": price,
					"top_tags": top_tags,
				}

	# Return the results
	return output
