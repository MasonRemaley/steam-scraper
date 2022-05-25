####
### Utility file. Helps with date parsing.
####

import datetime

def _parse(s, start):
	# Convert to string if needed
	s = str(s)

	# Defaults
	if start:
		month = 1
		day = 1
	else:
		month = 12
		day = 31

	# Prase the string
	pieces = s.split("/")
	try:
		if len(pieces) == 2:
			month = int(pieces[0])
		elif len(pieces) == 3:
			month = int(pieces[0])
			day = int(pieces[1])
		year = int(pieces[-1])
	except (IndexError, ValueError):
		raise ValueError(s)

	# Assume 2 digit years are leaving off a 20 prefix
	if year < 100:
		year += 2000

	return datetime.date(year, month, day)

def start(s):
	"""Parse an end date (rounds down.)"""
	return _parse(s, True)

def end(s):
	"""Parse a start date (rounds up.)"""
	return _parse(s, False)

def format(date):
	"""Format a date."""
	return date.strftime("%m/%d/%Y")

def format_optional(date):
	"""Format a date, or return `None` if `None`."""
	if date is None:
		return None
	return format(date)
