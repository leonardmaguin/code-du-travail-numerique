import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import re

from nltk import RegexpTokenizer

#articles_code = "results/articles_code.json"
code_tags_path = "results/code_tags.json"
fiches_sp_path = "ressources/fiches-sp-travail.json"

def search_article(output_json, manual_output_json, articles_code_dict, fiche_dict):

	fiche_data = {
		#"themes": val.get("themes", []),
		"tags": fiche_dict['tags'],
		"texte": fiche_dict.get('text',""),
		"refs": fiche_dict.get('refs',[]),
		"title": fiche_dict['title'],
	}
	fiche_data["all_text"] = fiche_data["texte"] + ' '.join(v["source"] for v in fiche_data["refs"])

	print("REFS :" ,fiche_data)

	manual_output_json[fiche_data["title"]] = []
	for el in fiche_data["tags"]:
		manual_output_json[fiche_data["title"]].append(el)

	output_json[fiche_data["title"]] = set()

	regexp = r"([LRD](?:\. )?[0-9]{3,6}-[0-9]{1,3}-?[0-9]{0,2})( à [LRD]?(\. )?[0-9]{3,6}-[0-9]{1,3}-?[0-9]{0,2})?"
	
	articles_matches = re.finditer(regexp, fiche_data["all_text"], re.MULTILINE)
	for matchNum, match in enumerate(articles_matches):
		if match.group(2):
			splited_match = match.group(2).split("-")
			last_article_number = splited_match[len(splited_match)-1]
			splited_match = match.group(1).split("-")
			first_article_number = splited_match[len(splited_match)-1]
			article_root = match.group(1)[:-len(first_article_number)].replace(". ", "")
			articles = []
			for i in range(int(first_article_number), int(last_article_number)+1):
				articles.append(article_root + str(i))
		else:
			articles = [match.group(1).replace(". ", "")]
		print(match.group(0), articles)

		for article in articles:
			codes = articles_code_dict.get(article, [])
			for el in codes:
				if el not in output_json[fiche_data["title"]]:
					output_json[fiche_data["title"]].add(el)
		#print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
	#print(articles)
	return output_json, manual_output_json

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

def match_tags(bytags_output_json, code, code_tag, fiches_sp):


	tag_texts = code_tag["tags"]
	words = []

	words_to_match = 0
	for index, text in enumerate(tag_texts):
		words.append(text.split(" "))
		words_to_match += len(words[index])
	print(words_to_match, tag_texts)
	for fiche in fiches_sp:
		words_matched = 0
		fiche_texte = fiche.get('text',"")
		for index, words_list in enumerate(words):
			for word in words_list:
				if (word in fiche_texte):
					words_matched += 1
		print(fiche['title'], words_to_match, words_matched)
		if (words_matched >= 0.8 * words_to_match): 
			print("ITS A MATCH!", fiche['title'], words_to_match, words_matched)
			bytags_output_json[fiche['title']].append(code)
	return bytags_output_json

	#toknizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
	#toknizer.tokenize(content_french)
	#>> ['John', 'Richard', 'Bond', ...,"l'", 'astronomie', '.']



if __name__ == "__main__":
	output_json = {}
	bytags_output_json = {}
	manual_output_json = {}
	with open(code_tags_path) as f:
		code_tags = json.load(f)

	"""
	for article in data.keys():
		#print(article)
		output_json = search(output_json, article, data[article])
	# Convert sets to lists
	for key in output_json:
		output_json[key] = list(output_json[key])
	with open('faq_code.json', 'w') as outfile:
		json.dump(output_json, outfile)
	#search(article=article)
	"""

	#prog = re.compile(regexp)

	with open(fiches_sp_path) as json_data:
		fiches_sp = json.load(json_data)
	for fiche in fiches_sp:
		bytags_output_json[fiche['title']] = []

	for key in code_tags.keys():
		#output_json, manual_output_json = search_article(output_json, manual_output_json, data, fiche)
		bytags_output_json = match_tags(bytags_output_json, key, code_tags[key], fiches_sp)

	for key in bytags_output_json:
		bytags_output_json[key] = list(bytags_output_json[key])
	#for key in output_json:
	#	output_json[key] = list(output_json[key])
	with open('results/fichessp_code_bytags.json', 'w') as outfile:
		json.dump(bytags_output_json, outfile)
	#with open('results/fichessp_code_byquotation.json', 'w') as outfile:
	#	json.dump(output_json, outfile)
	#with open('results/fichessp_code_bymanual.json', 'w') as outfile:
	#	json.dump(manual_output_json, outfile)