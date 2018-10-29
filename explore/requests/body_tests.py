body_0 = {
	  "query": {
	    "bool": {
	    #Celui ci prend une très grande importance
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

body_1 = {
	  "query": {
	    "bool": {
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