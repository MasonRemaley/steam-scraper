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
			'start': date.to_dict(args.start),
			'end': date.to_dict(args.end),
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
			title = game.find("span", class_="title").text

			released = game.find("div", class_="search_released")
			if released:
				released = released.text.strip()
				try:
					released = datetime.strptime(released, "%b %d, %Y").date()
					current_date = released
				except ValueError:
					released = None

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

			if released and (args.start <= released <= args.end):
				output["games"].append({
					"title": title,
					"released": date.to_dict(released),
					"reviews": reviews,
					"price": price,
					"top_tags": tags,
				})

	with open(args.output, 'w') as f:
		f.write(json.dumps(output, indent="\t"))

	print(f"Scraped data written to {args.output}")


# TODO: follower counts?
