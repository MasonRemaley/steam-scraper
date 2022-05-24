import requests
from bs4 import BeautifulSoup
import re
import time
import json

from tags import TAG_IDS
from tags import TAG_NAMES

def scrape(args):
	output = {
		'critera': {
			'tags': args.tag,
		},
		'games': [],
	}

	target_year = 2021
	current_year = float('inf')
	start = 0

	# TODO: output info on the search in the file
	while current_year >= target_year:
		try:
			tags = "%2C".join([str(TAG_IDS[tag]) for tag in args.tag])
		except KeyError as tag:
			print(f"Error: tag {tag} not found in 'tags.py'")
			return
		url = f"https://store.steampowered.com/search/?sort_by=Released_DESC&tags={tags}&category1=998&category3=2&os=win&start={start}&count=25"

		start += 25
		print(url)
		headers = {"Accept-Language": "en-US, en;q=0.5"}
		results = requests.get(url, headers=headers)


		soup = BeautifulSoup(results.text, "html.parser")
		games = soup.find_all("a", class_="search_result_row")


		for game in games:
			title = game.find("span", class_="title").text

			released = game.find("div", class_="search_released")
			if released:
				released = released.text.strip()
				try:
					released = time.strptime(released, "%b %d, %Y")
					released = {
						"month": released.tm_mon,
						"year": released.tm_year,
						"day": released.tm_mday,
					}
					current_year = released["year"]
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

			# TODO: make a private git repo for this!!
			# TODO: make sure these are in order!!
			tags = [TAG_NAMES[int(tag)] for tag in game["data-ds-tagids"][1:-1].split(",")]

			if current_year == target_year:
				output["games"].append({
					"title": title,
					"released": released,
					"reviews": reviews,
					"price": price,
					"top_tags": tags,
				})

	with open(args.output, 'w') as f:
		f.write(json.dumps(output, indent="\t"))

	print(f"Scraped data written to {args.output}")


# TODO: follower counts?
