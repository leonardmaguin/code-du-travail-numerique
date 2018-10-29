import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import re

esclient = Elasticsearch(['0.0.0.0'], port=9200)
articles_code = "results/articles_code.json"
faq_path = "ressources/faq.json"
faq_conventions_path = "ressources/faq-conventions-collectives.json"

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def search(output_json, article, codes):
	body = { 
		"query": {
			"bool" : {
				"must" : [{
		  "term": {
			  "source": "faq"
		  }
	  }, {
		  "term": {
			  "all_text": article
		  }
	  }]
	  }
	  }
	}
	#print(body)
	res = esclient.search(index="code_du_travail_numerique", body=body)['hits']
	#print(res)
	#keys = []
	print("HERE", article, codes, len(res['hits']))
	titres = []
	for el in res['hits']:
		#keys += el["_source"].keys()
		#titre.append(el["_source"]["title"])
		titre = el["_source"]["title"]
		#print(article, " : ", titre)
		if titre in output_json:
			for el in codes:
				#print("Stuck ?", codes)
				#if titre == "en cours de préavis, ai-je le droit à du temps rechercher un emploi?":
				#	print("Stuck!!", output_json[titre], el, output_json)
				if el not in output_json[titre]:
					output_json[titre].add(el)
		else:
			#print("Stuck 2 ?", codes)
			output_json[titre] = set(codes.copy())
		#print("Stuck 3 ?", output_json)
	return output_json
			
		#print("\nSTART---", (el if field == 'all' else (el['_source'][field] if field != 'tiext' else el['_source']['title'], el['_source']['text'])))
		#keys = list(set(keys))
	#print('-- -- -- \nHow many ? ', len(res['hits']), ' | keys :', keys)

def search_article(output_json, manual_output_json, articles_code_dict, faq_dict):

	faq_text = strip_html(faq_dict['reponse'])
	faq_data = {
		"themes": faq_dict.get("themes", []),
		"title": faq_dict['question'],
		"all_text": f"{faq_dict['question']} {faq_text} {faq_dict['theme']} {faq_dict['branche']}",
	}

	manual_output_json[faq_data["title"]] = []
	for el in faq_data["themes"]:
		manual_output_json[faq_data["title"]].append(el)

	output_json[faq_data["title"]] = set()

	regexp = r"[LRD](\. )?[0-9]{3,6}-[0-9]{1,3}-?[0-9]{0,2}"

	regexp_fiches = r"[LRD](\. )?[0-9]{3,6}-[0-9]{1,3}-?[0-9]{0,2}(( à )[LRD]?(\. )?[0-9]{3,6}-[0-9]{1,3}-?[0-9]{0,2})?"
	
	articles = re.finditer(regexp, faq_data["all_text"], re.MULTILINE)
	for matchNum, match in enumerate(articles):
		article = match.group(0).replace(". ", "")
		print(match.group(0), article)
		codes = articles_code_dict.get(article, [])
		for el in codes:
			if el not in output_json[faq_data["title"]]:
				output_json[faq_data["title"]].add(el)
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

	with open(faq_path) as json_data:
		faq = json.load(json_data)
	for val in faq:
		output_json, manual_output_json = search_article(output_json, manual_output_json, data, val)

	for key in output_json:
		output_json[key] = list(output_json[key])
	with open('results/faq_code_byquotation.json', 'w') as outfile:
		json.dump(output_json, outfile)
	with open('results/faq_code_bymanual.json', 'w') as outfile:
		json.dump(manual_output_json, outfile)