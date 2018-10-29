from search.extraction.synonyms.data import SYNONYMS


filters = {
        "french_elision": {
          "type": "elision",
          "articles_case": True,
          "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
        },
        "french_stop": {
          "type":       "stop",
          "stopwords":  "_french_" 
        },
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        },
        'synonyms': {
            'type': 'synonym',
            'synonyms': SYNONYMS,
        }
      }


analyzers = {
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
        },
        'path_analyzer_custom': {
          'tokenizer': 'tags'
          }
      }

code_du_travail_numerique_mapping = {
    'properties': {
        # Indicates the origin of the document, e.g. 'code_du_travail', 'fiches_service_public' etc.
        'source': {
          "type": "text",
          "analyzer": "default",
          "search_analyzer": "default"
        },
        # The local document slug
        'slug': {
          "type": "text",
          "analyzer": "default",
          "search_analyzer": "default"
        },
        # The source URL
        'url': {
            'type': 'text',
            'analyzer': 'standard',
        },
        "title": {
          "type": "text",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy" 
          # Useful to match articles by number, e.g. "R1227-7".
                #'whitespace': {
                #    'type': 'text',
                #    'analyzer': 'whitespace',
                #},
        },
        # A field that concatenate `title` and `text` fields.
        "all_text": {
          "type": "text",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy"
        },
        'text': {
          "type": "text",
          "analyzer": "french_heavy",
          "search_analyzer": "french_heavy"
        },
        # Currently only available for `Fiches service public`.
        'tags': {
          "type": "text",
          "analyzer": "default",
          "search_analyzer": "default"
        },
        # Currently only available for `Code du travail`.
        'path': {
            'type': 'text',
            'analyzer': 'path_analyzer_custom'
        },
    },
}

tokenizers = {
    'tags': {
      "type": "path_hierarchy",
      "delimiter": "/",
      "replacement": "/",
      "skip": 0,
      "reverse": True
    },
}