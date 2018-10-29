import sys
from elasticsearch import Elasticsearch
from elasticsearch import helpers
esclient = Elasticsearch(['0.0.0.0'], port=9200)

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
	                    "query": val,
	                    "operator": "and",
	                    "cutoff_frequency": 0.0007,
	                    "fuzziness": "AUTO"
	                  }
	                }
	              },
	              {
	                "match": {
	                  "all_text.french_stemmed": {
	                    "query": val,
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
	            "query": val,
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
	              "query": val,
	              "boost": 1500
	            }
	          }
	        },
	        {
	          "multi_match": {
	            "query": val,
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
	print(body)
	res = esclient.search(index="code_du_travail_numerique", body=body)['hits']
	print(res)
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





"""
{
      query: {
        bool: {
          must: [
            # Fuziness is ignored with multi_match's cross_fields.
            # https://github.com/elastic/elasticsearch/issues/6866
            # Put multi_match clause in standby, use an inner bool with 2 should clauses instead.
            # {
            #   multi_match: {
            #     query: val,
            #     fields: [
            #       'all_text.french_stemmed',
            #       'all_text.french_exact',
            #     ],
            #     operator: 'and',
            #     cutoff_frequency: 0.0007,
            #     type: 'cross_fields',
            #   },
            {
              bool: {
                should: [
                  {
                    match: {
                      'all_text.french_exact': {
                        query: val,
                        operator: 'and',
                        cutoff_frequency: 0.0007,
                        fuzziness: 'AUTO',
                      },
                    },
                  },
                  {
                    match: {
                      'all_text.french_stemmed': {
                        query: val,
                        operator: 'and',
                        cutoff_frequency: 0.0007,
                        fuzziness: 'AUTO',
                      },
                    },
                  },
                ],
              },
            },
          ],
          should: [
            {
              multi_match: {
                query: val,
                fields: ['title.french_stemmed', 'title.french_exact'],
                type: 'most_fields',
                boost: 2000,
              },
            },
            {
              match: {
                'all_text.shingle': {
                  query: val,
                  boost: 1500,
                },
              },
            },
            {
              multi_match: {
                query: val,
                fields: ['path.french_stemmed', 'path.french_exact'],
                type: 'most_fields',
                boost: 500,
              },
            },
            # Temporarily put "fonction publique" and "agent public" results in a less prominent position.
            # todo: add a disclaimer
            {
              query_string: {
                query:
                  '(title.shingle:"fonction publique") OR (title.shingle:"agent public")',
                boost: -2000,
              },
            },
          ],
        },
      },
      highlight: {
        order: 'score',
        pre_tags: ['<mark>'],
        post_tags: ['</mark>'],
        fragment_size: 40,
        fields: {
          'title.french_stemmed': {},
          'title.french_exact': {},
          'all_text.french_stemmed': {},
          'all_text.french_exact': {},
          'all_text.shingle': {},
          'path.french_stemmed': {},
          'path.french_exact': {},
        },
      },
    }

    """