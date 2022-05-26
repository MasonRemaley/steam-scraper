import json

def load(path):
	with open(path, 'r') as f:
		return json.loads(f.read())

def union(*dicts):
	dicts = list(dicts)

	if len(dicts) == 0:
		return {}

	if len(dicts) == 1:
		return dict(dicts.pop())

	if len(dicts) == 2:
		a = dicts.pop()
		b = dicts.pop()
		return dict(a, **b)

	return union(
		union(dicts.pop(), dicts.pop()),
		*dicts,
	)

def delete(parent_dict, child_dict):
	parent_dict = parent_dict.copy()
	for key in child_dict.keys():
		if key in parent_dict:
			del parent_dict[key]
	return parent_dict

def intersect(*dicts):
	dicts = list(dicts)

	if len(dicts) == 0:
		return {}

	if len(dicts) == 1:
		return dict(dicts.pop())

	if len(dicts) == 2:
		a = dicts.pop()
		b = dicts.pop()
		return {k:a[k] for k in a if k in b}

	return intersect(
		intersect(dicts.pop(), dicts.pop()),
		*dicts,
	)


def save(games, path):
	with open(path, 'w') as f:
		f.write(json.dumps(games, indent="\t"))

def min_price(games, min_price):
	return { k : v for (k, v) in games.items() if v["price"] is not None and v["price"] >= min_price }

def min_reviews(games, min_reviews):
	return { k : v for (k, v) in games.items() if v["reviews"] is not None and v["reviews"] >= min_reviews }

def without_top_tag(games, tag):
	return { k : v for (k, v) in games.items() if tag not in v["top_tags"] }