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

	return intersection(
		intersection(dicts.pop(), dicts.pop()),
		*dicts,
	)

def save(games, path):
	with open(path, 'w') as f:
		f.write(json.dumps(games, indent="\t"))
