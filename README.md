# Steam Market Analysis

Usage:
```
python3 main.py --help
```

# Warning

This tool starts with the present year and works backwards. If you input, say, year 2000, it will
attempt to search through all games released with the given tags between now and 2000. I don't know
if Steam gets upset if they realize you're scraping, doing that is certainly a way to find out.

# Installation

TODO

# To Do
- Make it easier to iteratively filter list by hand, don't aggregate away the data--just automate
  the painful parts
- If we want to look at old years, we could jump more pages back
- Check for early access
- Check follower counts?
