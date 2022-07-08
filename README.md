# Steam Scraper

# Installation

```py
pip3 install -r requirements.txt
```

# Usage

Scraping example:
```py
import steam_scraper as ss

# Months can also be inputted as strings (m/d/y or m/y), tags can be a list
rd = ss.scrape("Roguelike Deckbuilder", start=2021, end=2021)
rl = ss.scrape("Rogue-like", start=2021, end=2021)
rt = ss.scrape("Rogue-lite", start=2021, end=2021)
cg = ss.scrape("Card Game", start=2021, end=2021)
cb = ss.scrape("Card Battler", start=2021, end=2021)

ss.save(rd, "out/roguelike-deckbuilder.json")
ss.save(rl, "out/rogue-like.json")
ss.save(rt, "out/rogue-lite.json")
ss.save(cg, "out/card-game.json")
ss.save(cb, "out/card-battler.json")
```

Analysis example:
```py
import steam_scraper as ss

rd = ss.load("out/roguelike-deckbuilder.json")
rl = ss.load("out/rogue-like.json")
rt = ss.load("out/rogue-lite.json")
cg = ss.load("out/card-game.json")
cb = ss.load("out/card-battler.json")

cg = ss.union(rd, cg, cb)
rl = ss.union(rd, rl, rt)
rc = ss.intersect(cg, rl)

# At this point you'll probably want to filter this list a bit, and then save it an look over it
# manually to make sure it looks right/remove any irrelevant games.
rc = ss.min_price(rc, 14.99)
rc = ss.min_reviews(rc, 10)
rc = ss.without_top_tag(rc, "Early Access") # Note: misses some early access games right now
ss.save(rc, "out/rc-filtered.json")

# Once you're ready for analysis, you can load it back in if you made any changes and analyze it.
rc = ss.load("out/rc-filtered.json")


ss.analyze(rc)
```

# Warning

This tool starts with the present year and works backwards. If you input, say, year 2000, it will
attempt to search through all games released with the given tags between now and 2000. I don't know
if Steam gets upset if they realize you're scraping, doing that is certainly a way to find out.



# To Do
- Does early access filter always work when searching only top tags?
	- It doesn't...
- Pick some games and double check their data manually, we almost got reviews off by a large factor
  due to commas lol...
- Filter based on descriptions? Or even just mark them?
- Also estimate games going on sale?
- Rename revenue to estimated revenue
- Maybe include upper and lower estimates for revenue
- Add a way to remove below a price in the repl instead of in analysis
- In the process of switching over to a completely repl based approach
	- better error handling for repl approach?
- Add some tests to filter.py, I *think* I got it right
- Add more complicated tag processing (e.g. we should be able to check for
  or(and(or(roguelike, roguelite), or(card game, deckbuilding, card battler)), roguelike deckbuilder),
  or search descriptions
	- Maybe the answer is that we need this to be a repl tool..?
	- Wait can we search for all with any of these tags and then filter later?
	- Oh interesting, we /can't/ do "or" on steam search can we?
	- Okay we need to actually combine multiple datasets
	- Make it easier to print the dicts so you can see what you're doing (wrap them in some other type?)
- Make it easier to iteratively filter list by hand, don't aggregate away the data--just automate
  the painful parts
- If we want to look at old years, we could jump more pages back
- Check follower counts?
- Add back top tags check?
- Document keys.js
