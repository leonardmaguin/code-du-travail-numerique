from search.extraction.synonyms.data import SYNONYMS


  "settings": {
    "analysis": {
      "filter": {
        "french_elision": {
          "type": "elision",
          "articles_case": true,
          "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
        },
        "french_stop": {
          "type":       "stop",
          "stopwords":  "_french_" 
        },
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        }
      },
      "analyzer": {
        "french_heavy": {
          "tokenizer": "icu_tokenizer",
          "filter": [
            "french_elision",
            "lowercase",
            "french_stop",
            "icu_folding",
            "french_stemmer"
          ]
        },
        "french_light": {
          "tokenizer": "icu_tokenizer",
          "filter": [
            "french_elision",
            "lowercase",
            "french_stop",
            "icu_folding"
          ]
        }
      }
    }
  },
  "mappings": {
    "file": {
      "properties": {
        "project_id": {
          "type": "string",
          "analyzer": "default",
          "search_analyzer": "default"
        },
        "title": {
          "type": "string",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy"
        },
        "content": {
          "type": "text",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy"
        },
        "ori_path": {
          "type": "text",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy"
        }        
      }
    }
  }
}
'
