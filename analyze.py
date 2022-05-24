import statistics
import json

def analyze(args):
	with open(args.input, 'r') as f:
		games = json.loads(f.read())

	def filter(game):
		if game["released"] is None:
			return False
		if game["price"] is None:
			return False
		if game["price"] <= 9:
			return False
		if game["reviews"] < 10:
			return False

		is_roguelike = "Rogue-like" in game["top_tags"] or "Rogue-lite" in game["top_tags"]
		is_deckbuilder = "Roguelike Deckbuilder" in game["top_tags"] or "Deckbuilding" in game["top_tags"]

		# TODO: check for early access? check descriptions for keywords, this is maybe too harsh?
		return is_roguelike and is_deckbuilder

	games = [game for game in games if filter(game)]

	for game in games:
		if game["price"]:
			game["revenue"] = round(game["reviews"] * 50 * game["price"] * .65)
		else:
			game["revenue"] = 0

	games.sort(key=lambda g: g["revenue"])

	# print(json.dumps(games, indent='\t'))
	# TODO: lets save all the tags, and have a way to filte rbased on top 5 tags or something,
	# i mean check maybe these ARE rogueliek deckbuilders but idk

	for game in games:
		print(f"{game['title']}:\t\t${int(game['revenue']):,d}")

	revenue = [game["revenue"] for game in games]
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