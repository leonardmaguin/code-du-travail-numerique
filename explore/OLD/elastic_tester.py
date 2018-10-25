import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
esclient = Elasticsearch(['0.0.0.0'], port=9200)

def body_insert_value(body, value):
    new_body = body
    for k, v in body.items():
        print(k,v)
        if isinstance(v, dict):
            new_body[k] = body_insert_value(v, value)
        else:
            if isinstance(v, list):
                for list_item in v:
                    if isinstance(list_item, dict):
                        body_insert_value(list_item, value)
            else:
                if isinstance(v, str):
                    v = v.replace("INSERT VALUE HERE", value)
                    print("ICI {0} : {1}".format(k, v))
                    return v
    return new_body

def search(val, field='all'):
	body = {
	  "query": {
	    "bool": {
	      "must": [
	        {
	          "bool": {
	            "should": [
	              {
	                "match": {
	                  "all_text.french_exact": {
	                    "query": "INSERT VALUE HERE",
	                    "operator": "and",
	                    "cutoff_frequency": 0.0007,
	                    "fuzziness": "AUTO"
	                  }
	                }
	              },
	              {
	                "match": {
	                  "all_text.french_stemmed": {
	                    "query": "INSERT VALUE HERE",
	                    "operator": "and",
	                    "cutoff_frequency": 0.0007,
	                    "fuzziness": "AUTO"
	                  }
	                }
	              }
	            ]
	          }
	        }
	      ],
	      "should": [
	        {
	          "multi_match": {
	            "query": "INSERT VALUE HERE",
	            "fields": [
	              "title.french_stemmed",
	              "title.french_exact"
	            ],
	            "type": "most_fields",
	            "boost": 2000
	          }
	        },
	        {
	          "match": {
	            "all_text.shingle": {
	              "query": "INSERT VALUE HERE",
	              "boost": 1500
	            }
	          }
	        },
	        {
	          "multi_match": {
	            "query": "INSERT VALUE HERE",
	            "fields": [
	              "path.french_stemmed",
	              "path.french_exact"
	            ],
	            "type": "most_fields",
	            "boost": 500
	          }
	        },
	        {
	          "query_string": {
	            "query": "(title.shingle:\"fonction publique\") OR (title.shingle:\"agent public\")",
	            "boost": -2000
	          }
	        }
	      ]
	    }
	  },
	  "highlight": {
	    "order": "score",
	    "pre_tags": [
	      "<mark>"
	    ],
	    "post_tags": [
	      "</mark>"
	    ],
	    "fragment_size": 40,
	    "fields": {
	      "title.french_stemmed": {},
	      "title.french_exact": {},
	      "all_text.french_stemmed": {},
	      "all_text.french_exact": {},
	      "all_text.shingle": {},
	      "path.french_stemmed": {},
	      "path.french_exact": {}
	    }
	  },
	"size":1000
	}

	body = body_insert_value(body, val)
	print("HEREWEARE", body)

	res = esclient.search(index="code_du_travail_numerique", body=body)['hits']
	keys = []
	for el in res['hits']:
		keys += el["_source"].keys()
		print("\nSTART---", (el if field == 'all' else (el['_source'][field] if field != 'tiext' else el['_source']['title'], el['_source']['text'])))
		keys = list(set(keys))
	print('-- -- -- \nHow many ? ', len(res['hits']), ' | keys :', keys)

if __name__ == "__main__":
	field = sys.argv[1]
	arg = str(' '.join(sys.argv[2:]))
	search(str(arg), field=field)

