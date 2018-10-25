from search.extraction.synonyms.data import SYNONYMS


filters = {
    # Normalize acronyms so that no matter the format, the resulting token will be the same.
    # E.g.: SmiC => S.M.I.C. => SMIC => smic.
    'acronyms': {
        'type': 'word_delimiter',
        'catenate_all': True,
        'generate_word_parts': False,
        'generate_number_parts': False,
    },
    'french_elision': {
        'type': 'elision',
        'articles_case': True,
        'articles': [
        ],
    },
    'french_stemmer': {
        'type': 'stemmer',
        'language': 'light_french',
    },
    'french_stop': {
        'type': 'stop',
        'stopwords': '_french_',
    },
    'synonyms': {
        'type': 'synonym',
        'synonyms': SYNONYMS,
    },
}

analyzers = { 
    'french_stemmed': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'icu_tokenizer',
        'filter': [
            'french_elision',
            'icu_folding',
            'lowercase',
            'acronyms',
            'synonyms',
            'french_stop',
            'french_stemmer',
        ],
    },
    'french_exact': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'icu_tokenizer',
        'filter': [
            'french_elision',
            'icu_folding',
            'lowercase',
            'acronyms',
            'synonyms',
            'french_stop',
        ],
    },
    'shingle': {
        'type': 'custom',
        'char_filter': ['html_strip'],
        'tokenizer': 'icu_tokenizer',
        'filter': [
            'french_elision',
            'icu_folding',
            'lowercase',
            'acronyms',
            'synonyms',
            'french_stop',
            'shingle',
        ],
    },
    'path_analyzer_custom': {
        'tokenizer': 'tags',
    },
}

tokenizers = {
    'tags': {
        'type': 'path_hierarchy',
    },
}

code_du_travail_numerique_mapping = {
    'properties': {
        # Indicates the origin of the document, e.g. 'code_du_travail', 'fiches_service_public' etc.
        'source': {
            'type': 'text',
            'fielddata': True,
            'analyzer': 'keyword',
        },
        # The local document slug
        'slug': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        # The source URL
        'url': {
            'type': 'text',
            'analyzer': 'keyword',
        },
        'title': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_stemmed': {
                    'type': 'text',
                    'analyzer': 'french_stemmed',
                },
                'french_exact': {
                    'type': 'text',
                    'analyzer': 'french_exact',
                },
                'shingle': {
                    'type': 'text',
                    'analyzer': 'shingle',
                },
                # Useful to match articles by number, e.g. "R1227-7".
                'whitespace': {
                    'type': 'text',
                    'analyzer': 'whitespace',
                },
            },
        },
        'text': {
            'type': 'text',
            'analyzer': 'standard',
            'fields': {
                'french_stemmed': {
                    'type': 'text',
                    'analyzer': 'french_stemmed',
                },
                'french_exact': {
                    'type': 'text',
                    'analyzer': 'french_exact',
                },
                'shingle': {
                    'type': 'text',
                    'analyzer': 'shingle',
                },
            },
        },
    },
}
