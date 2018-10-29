def wording (str_1, search_val):
	if len(str_1) == 0:
		return 0
	"""

	This function calculates a wording distance between 'val' and certain names.
	It is ranged between 0 and 1, with a x^3 curve.
	This distance is used in sorting.

	"""
	def _wording (text, match):
		tokens = word_tokenize(text.lower())
		if len(tokens) == 0 : return 0
		uples = [el for el in tokens if el not in stopwords]
		duples = [tokens[el] + ' ' + tokens[el+1] for el in range(len(tokens) - 1)]
		truples = [tokens[el] + ' ' + tokens[el+1] + ' ' + tokens[el+2] for el in range(len(tokens) - 2)]
		quadruples = [tokens[el] + ' ' + tokens[el+1] + ' ' + tokens[el+2] + ' ' + tokens[el+3] for el in range(len(tokens) - 3)]
		quintuples = [tokens[el] + ' ' + tokens[el+1] + ' ' + tokens[el+2] + ' ' + tokens[el+3] + ' ' + tokens[el+4] for el in range(len(tokens) - 4)]
		dist = 10
		for el in uples + duples + truples + quadruples + quintuples:
			dist = min(fuzzydist(match, el), dist)
		dist = (dist/len(match))
		res = 1 if dist == 0 else (1 - (dist)) * (1 - (dist))
		return res - min(0, abs(len(text) - len(match))) * weights['wording_len_malus']
	str_1 = str_1.replace('-', ' ')
	search_val = search_val.lower()
	try:
		default = _wording(str_1, search_val)
	except Exception as e:
		print('ERROR _wording >>', e, ' | default :', str_1, search_val)
		default = 0

	return max(default, 0)#max(stemmed, lemmed, default, 0)