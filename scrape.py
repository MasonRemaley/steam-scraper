import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime

import date

from tags import TAG_IDS
from tags import TAG_NAMES

def scrape(args):
	output = {
		'criteria': {
			'tags': args.tag,
			'start': date.format(args.start),
			'end': date.format(args.end),
		},
		'games': [],
	}

	target_year = 2021
	current_date = args.end
	result_index = 0

	# TODO: output info on the search in the file
	while current_date > args.start:
		try:
			tags = "%2C".join([str(TAG_IDS[tag]) for tag in args.tag])
		except KeyError as tag:
			print(f"Error: tag {tag} not found in 'tags.py'")
			return
		max_results = 25 # The minimum that's respected
		url = f"https://store.steampowered.com/search/?sort_by=Released_DESC&tags={tags}&category1=998&category3=2&os=win&start={result_index}&count={max_results}"

		# TODO: add the amount actually found instead just in case
		print(url)
		headers = {"Accept-Language": "en-US, en;q=0.5"}
		results = requests.get(url, headers=headers)


		soup = BeautifulSoup(results.text, "html.parser")
		games = soup.find_all("a", class_="search_result_row")
		result_index += len(games)


		for game in games:
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
				reviews = int(re.search(r"(\d+) user reviews", reviews["data-tooltip-html"])[1])
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

			tags = [TAG_NAMES[int(tag)] for tag in game["data-ds-tagids"][1:-1].split(",")]

			if release_date and (args.start <= release_date <= args.end):
				output["games"].append({
					"title": title,
					"store_page": store_page,
					"release_date": date.format_optional(release_date),
					"reviews": reviews,
					"price": price,
					"top_tags": tags,
				})

	output["games"].reverse()

	with open(args.output, 'w') as f:
		f.write(json.dumps(output, indent="\t"))

	print(f"Scraped data written to {args.output}")


# TODO: follower counts?
