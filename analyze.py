import statistics
import json

_boxleiter_number = 30
_steam_cut_sales_taxes = 0.65

def analyze(args):
	with open(args.input, 'r') as f:
		data = json.loads(f.read())

	# TODO: check for early access? check descriptions for keywords, this is maybe too harsh?
	# TODO: output manually and allow filtering by hand
	def _filter(game):
		return set(data["criteria"]["tags"]).issubset(game["top_tags"])
	games = [game for game in data["games"] if _filter(game)]

	for game in data["games"]:
		if game["price"]:
			copies_sold = game["reviews"] * _boxleiter_number
			game["revenue"] = round(copies_sold * game["price"] * _steam_cut_sales_taxes)
		else:
			game["revenue"] = 0

	games.sort(key=lambda g: g["revenue"])

	# print(json.dumps(games, indent='\t'))
	# TODO: lets save all the tags, and have a way to filte rbased on top 5 tags or something,
	# i mean check maybe these ARE rogueliek deckbuilders but idk

	for game in data["games"]:
		print(f"{game['title']}:\t\t${int(game['revenue']):,d}")

	revenue = [game["revenue"] for game in data["games"]]
	if len(revenue) > 2:
		quantiles = statistics.quantiles(revenue)
		print(f"25%: ${int(quantiles[0]):,d}")
		print(f"50%: ${int(quantiles[1]):,d}")
		print(f"75%: ${int(quantiles[2]):,d}")
	print(f"total: {len(revenue)}")
	# print(f"{game['revenue']:,d}")
	# print(games)
	# TODO:
	# - pagify (we know how now!)
	# - stop when we get to a certain year
	# - skip stuff (or filter later) based on price/reviews
	# - save some data to disk and figure out regexes to get the numbers out
	# - make it easier to search, output to csv or print nicesly, calcualte averages, etc
	# - maybe save results in intermediate step so we don't query over and over
	# - add store page links