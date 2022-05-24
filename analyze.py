import statistics
import json

_boxleiter_number = 30
_steam_cut_sales_taxes = 0.65

def analyze(args):
	with open(args.input, 'r') as f:
		data = json.loads(f.read())

	def _filter(game):
		if game["reviews"] < args.min_reviews:
			return False

		if not args.ignore_top_tags and not set(data["criteria"]["tags"]).issubset(game["top_tags"]):
			return False

		return True

	data["games"] = [game for game in data["games"] if _filter(game)]

	for game in data["games"]:
		if game["price"]:
			copies_sold = game["reviews"] * _boxleiter_number
			game["revenue"] = round(copies_sold * game["price"] * _steam_cut_sales_taxes)
		else:
			game["revenue"] = 0

	data["games"].sort(key=lambda g: g["revenue"])

	for game in data["games"]:
		print(f"{game['title']}:\t\t${int(game['revenue']):,d}")

	revenue = [game["revenue"] for game in data["games"]]
	if len(revenue) > 2:
		quantiles = statistics.quantiles(revenue)
		print(f"25%: ${int(quantiles[0]):,d}")
		print(f"50%: ${int(quantiles[1]):,d}")
		print(f"75%: ${int(quantiles[2]):,d}")
	print(f"total: {len(revenue)}")
