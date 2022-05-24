import argparse
import datetime

import date
from scrape import scrape
from analyze import analyze

parser = argparse.ArgumentParser(description="Steam market analyzer. First scrape data from Steam, then analyze the scraped data.")

subparsers = parser.add_subparsers(dest="command")

scrape_command = subparsers.add_parser("scrape", help="scrape new data")
scrape_command.add_argument("output", metavar="OUT", help="scraped data path")
scrape_command.add_argument("-t", "--tag", action="append", help="a steam tag to add to the search", required=True)
scrape_command.add_argument(
	"-s",
	"--start",
	type=date.start,
	help="the date to start the search at [[d/]m/]yy",
	required=True,
)
scrape_command.add_argument(
	"-e",
	"--end",
	type=date.end,
	help="the date to end the search at [[d/]m/]yy",
	required=True,
)

analyze_command = subparsers.add_parser("analyze", help="analyze scraped data")
analyze_command.add_argument("input", metavar="IN", help="scraped data path")

args = parser.parse_args()

if args.command == "scrape":
	scrape(args)
elif args.command == "analyze":
	analyze(args)