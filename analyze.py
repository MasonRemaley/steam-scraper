####
### Analysis implementation.
####

import statistics

_boxleiter_number = 38
_steam_cut_sales_taxes = 0.65

def analyze(data, min_reviews=10):
	# Estimate revenue
	data = list(data.values())
	for game in data:
		if game["price"]:
			copies_sold = game["reviews"] * _boxleiter_number
			game["revenue"] = round(copies_sold * game["price"] * _steam_cut_sales_taxes)
		else:
			game["revenue"] = 0
	data.sort(key=lambda g: g["revenue"])


	# Output the game and revenue list
	max_title_len = max(len(game["title"]) for game in data)
	revenue_strings = [f"${int(game['revenue']):,d}" for game in data]
	max_revenue_len = max(len(revenue_string) for revenue_string in revenue_strings)

	print("# Games Analyzed")
	for (game, revenue) in zip(data, revenue_strings):
		print(f"{revenue.ljust(max_revenue_len)} {game['title'].ljust(max_title_len)}")
	print()

	# Output the quantiles
	revenue = [game["revenue"] for game in data]
	print("# Revenue Quantiles")
	if len(revenue) > 2:
		quantiles = statistics.quantiles(revenue)
		print(f"25%: ${int(quantiles[0]):,d}")
		print(f"50%: ${int(quantiles[1]):,d}")
		print(f"75%: ${int(quantiles[2]):,d}")
	print()
	print(f"({len(revenue)} games analyzed)")
