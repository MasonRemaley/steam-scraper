import datetime

def _parse(s, start):
	pieces = s.split("/")

	try:
		try:
			day = int(pieces[-3])
		except IndexError:
			if start:
				day = 1
			else:
				day = 31

		try:
			month = int(pieces[-2])
		except IndexError:
			if start:
				month = 1
			else:
				month = 12

		year = int(pieces[-1])
	except (IndexError, ValueError):
		raise ValueError(s)

	# Assume 2 digit years are leaving off a 20 prefix
	if year < 100:
		year += 2000

	return datetime.date(year, month, day)

def start(s):
	return _parse(s, True)

def end(s):
	return _parse(s, False)

def format(date):
	return date.strftime("%m/%d/%Y")

def format_optional(date):
	if date is None:
		return None
	return format(date)

