# Steam Scraper

# Installation

```py
pip3 install -r requirements.txt
```

# Usage

Example usage:
```sh
python3 main.py scrape -t "Roguelike Deckbuilder" out/roguelike-deckbuilders.json --start 21 --end 21
python3 main.py scrape -t "Rogue-like"  out/rogue-like.json --start 21 --end 21
python3 main.py scrape -t "Rogue-lite"  out/rogue-lite.json --start 21 --end 21
python3 main.py scrape -t "Card Game"  out/card-game.json --start 21 --end 21
python3 main.py scrape -t "Card Battler"  out/card-battler.json --start 21 --end 21

python3
> import filter as f
>
> rd = f.load("out/roguelike-deckbuilders.json")
> rl = f.load("out/rogue-like.json")
> rt = f.load("out/rogue-lite.json")
> cg = f.load("out/card-game.json")
> cb = f.load("out/card-battler.json")
>
> card_games = f.union(rd, cg, cb)
> roguelikes = f.union(rd, rl, rt)
> roguelike_cardgames = f.intersection(card_games, roguelikes)
> 
> filter.save(roguelike_cardgames, "out/roguelike-cardgames.json")
> 
> import analyze as a
> a.analyze(roguelike_cardgames)
> # (output printed here)
>
> exit()
python3 main.py analyze out/roguelike-cardgames.json
```

More info:
```sh
python3 main.py --help
```

# Warning

This tool starts with the present year and works backwards. If you input, say, year 2000, it will
attempt to search through all games released with the given tags between now and 2000. I don't know
if Steam gets upset if they realize you're scraping, doing that is certainly a way to find out.



# To Do
- In the process of switching over to a completely repl based approach
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
- Check for early access
- Check follower counts?