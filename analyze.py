####
### Analysis implementation.
####

import statistics
import json

_boxleiter_number = 30
_steam_cut_sales_taxes = 0.65

def analyze(args):
	# Read the data file
	with open(args.input, 'r') as f:
		data = json.loads(f.read())

	# Filter out games that we don't want to analyze
	def _filter(game):
		if game["reviews"] < args.min_reviews:
			return False

		if (not args.ignore_top_tags
			and not set(data["criteria"]["tags"]).issubset(game["top_tags"])):
			return False

		if game["price"] == 0 or game["price"] is None:
			return False

		return True
	data["games"] = [game for game in data["games"] if _filter(game)]

	# Estimate revenue
	for game in data["games"]:
		if game["price"]:
			copies_sold = game["reviews"] * _boxleiter_number
			game["revenue"] = round(copies_sold * game["price"] * _steam_cut_sales_taxes)
		else:
			game["revenue"] = 0
	data["games"].sort(key=lambda g: g["revenue"])


	# Output the game and revenue list
	max_title_len = max(len(game["title"]) for game in data["games"])
	revenue_strings = [f"${int(game['revenue']):,d}" for game in data["games"]]
	max_revenue_len = max(len(revenue_string) for revenue_string in revenue_strings)

	print("# Games Analyzed")
	for (game, revenue) in zip(data["games"], revenue_strings):
		print(f"{revenue.ljust(max_revenue_len)} {game['title'].ljust(max_title_len)}")
	print()

	# Output the quantiles
	revenue = [game["revenue"] for game in data["games"]]
	print("# Revenue Quantiles")
	if len(revenue) > 2:
		quantiles = statistics.quantiles(revenue)
		print(f"25%: ${int(quantiles[0]):,d}")
		print(f"50%: ${int(quantiles[1]):,d}")
		print(f"75%: ${int(quantiles[2]):,d}")
	print()
	print(f"({len(revenue)} games analyzed)")
