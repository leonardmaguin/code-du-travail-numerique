# Sources des données

- FAQ
- Fichiers complets LegiFrance et/ou extraction Legilibre
- Tags fournis par ePoseidon
- BDCC : conventions collectives
- ngAccord : accords entreprise
- courriers-types
- outils

# Fichiers

- `code_bfc.json` : fichier de questions-réponses élaborées par la DIRECCTE de Bourgogne-Franche-Comté (daté de juin 2017)

- `code_du_travail/`

    - `code-du-travail-2018-03-13.pdf` : PDF officiel du code du travail (legilibre)
    - `code-du-travail-2018-01-01.json` : code du travail au format JSON issu de [legi.py](https://github.com/Legilibre/legi.py)
    - `source_eposeidon/nomenclatures_*.xml` : taggages des articles du code du travail (depuis appli DGT ePoseidon)
    - `nomenclatures-*.json` : conversion des XML ePoseidon en JSON

- `faq.json` : questions fréquentes, reformulées par les services de renseignement des DIRECCTE

- `fiches_ministere_travail/fiches-min-travail.json` : extraction fiches [ministère du travail](http://travail-emploi.gouv.fr/mot/fiches-pratiques-du-droit-du-travail?max_articles=400)

- `fiches_service_public/fiches-sp-travail.json` : extraction fiches "vos droits" travail [service-public.fr](https://www.data.gouv.fr/fr/datasets/service-public-fr-guide-vos-droits-et-demarches-particuliers/)

- `thesaurus/TESS.json` : Thesaurus Travail Emploi Santé Solidarité

- `synonyms.json` : liste de synonymes [élaborée à la main](https://github.com/SocialGouv/code-du-travail-explorer/issues/56)



# Génération des fichiers JSON

## Obtenir un fichier JSON depuis un XML ePoseidon

Vérifier le chemin du XML dans la constante `INPUT_XML` du fichier `code_du_travail/eposeidon_script/index.js`, puis :

```
$ cd dataset/code_du_travail/eposeidon_script
$ npm --version
5.10.0
$ node --version
v9.11.2
$ npm install
$ node index.js > ../nomenclatures-`date +%Y%m%d`.json
```

## Obtenir un fichier JSON des fiches du ministère du travail

```
$ cd dataset/fiches_ministere_travail
$ node ministere-travail-extract-fiches.js > fiches-min-travail.json
```

## Obtenir un fichier JSON des fiches du service public
Recupérer les archives 
- https://www.data.gouv.fr/fr/datasets/service-public-fr-guide-vos-droits-et-demarches-particuliers/
- https://www.data.gouv.fr/fr/datasets/service-public-fr-guide-vos-droits-et-demarches-professionnels-entreprises/
et extraire les fichiers dans le dossiers `dataset/fiches_service_public/data`

```
$ cd dataset/fiches_service_public
$ node service-public-extract-fiches.js > fiches-sp-travail.json
```


## Schema des donnees outils.json, courriers-type.json 

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#", 
  "title": "Contenu rédigés du code du travail",
  "description": "A code-du-travail-content-FF",
  "type": "object",
  "properties": {
    "questions": {
      "description":"une liste de questions à laquelle le contenu répond",
      "type": "Array",
      "items": {
        "type": "string"
      },
    },
    "theme": {
      "description":"le theme de la question",
      "type": "string",
    },
    "themes": {
      "description":"une liste d'identifiant eposeidon auquel le contenu correspond",
      "type": "array",
      "items": {
        "type": "number"
      },
    },
    "branche": {
      "description":"la branche qui s'applique pour cette question",
      "type": "string"
     },
    "source":{
      "description":"le service qui a fourni cette information",
      "type": "string"
     },
    "date":{
      "description":"la date de publication de cette information",
      "type": "string"
    },
    "type_de_contrat":{
      "description":"Les types de contrat auquels le contenu correspond",
      "type": "array",
      "items": {
        "type": "string"
      },
    },
    "travailleur_particulier":{
      "description":"Les cas de travailleur particuliers auquels le contenu correspond",
      "type": "array",
      "items": {
        "type": "string"
      },
    },
    "catégorie":{
      "description":"Les catégorie de salarié auquels le contenu correspond",
      "type": "array",
      "items": {
        "type": "string"
      },
    },
    "profil":{
      "description":"Les profil (employeur / salarié) auquels le contenu correspond",
      "type": "array",
      "items": {
        "type": "string"
      },
    },
  },
  "required": ["date", "theme", "themes"]
}

```
