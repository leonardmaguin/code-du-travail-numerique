import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import re

articles_code = "results/articles_code.json"
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




if __name__ == "__main__":
	output_json = {}
	manual_output_json = {}
	with open(articles_code) as f:
		data = json.load(f)
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
	for val in fiches_sp:
		output_json, manual_output_json = search_article(output_json, manual_output_json, data, val)

	for key in output_json:
		output_json[key] = list(output_json[key])
	with open('results/fichessp_code_byquotation.json', 'w') as outfile:
		json.dump(output_json, outfile)
	with open('results/fichessp_code_bymanual.json', 'w') as outfile:
		json.dump(manual_output_json, outfile)