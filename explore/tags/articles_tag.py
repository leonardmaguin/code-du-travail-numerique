import pandas as pd
import json

themes_file = "themev4.tsv"

code_row = "code"
articles_row = "Articles"
tags_rows = "tag_n"

def compute_articles_tags_json():
	df = pd.read_csv(themes_file, sep='\t')


	print(df.describe())
	df.head()
	columns = list(df.keys())
	print(df[0:1])
	print(df[1:2])
	#print(list(df.values()))
	print("LOOPING")

	output_json = {}
	output_json_articles = {}

	df = df.fillna(0)

	for index, row in df.iterrows():
		#print(row)
		#print()
		#row = row.fillna(0)
		code = row[code_row]
		if(row[articles_row] != 0):
			articles = row[articles_row].split("; ")
		else:
			articles = []
		print(row)
		tags = []

		for i in range(7, 0, -1):
			column_name = tags_rows.replace("n", str(i))
			if(row[column_name] != 0):
				tags.append(row[column_name])
				print(column_name, row[column_name])

		output_json[code] = {
			"articles" : articles,
			"tags" : tags
		}

		for article in articles:
			if article in output_json_articles:
				output_json_articles[article].append(code)
			else:
				output_json_articles[article] = [code]

	print(output_json)
	with open('code_tags.json', 'w') as outfile:
		json.dump(output_json, outfile)
	with open('articles_code.json', 'w') as outfile:
		json.dump(output_json_articles, outfile)





if __name__ == "__main__":
	compute_articles_tags_json()




"""

import pandas as pd
import nltk
import numpy as np
from nltk.corpus import wordnet
from elasticsearch import Elasticsearch
from nltk.metrics import edit_distance
import os
import config

for j, df in enumerate(df_heur[0:]):
    print("HEUR83")
    block1 = np.unique(list(df["Block1_op"]))
    block2 = np.unique(list(df["Block2_op"]))
    block3 = np.unique(list(df["Block3_op"]))
    block4 = np.unique(list(df["Block4_op"]))

    def f(x, block):
        distances = []
        for item in block:
            try:
                distances.append(edit_distance(x.lower(), item.replace("+", "").strip().lower()))
            except:
                distances.append(999)

        return block[distances.index(min(distances))]

    # On relie chaque élément de op aux éléments correspondants de ex grâce à une distance
    df["Block1_ex_stem"] = df["Block1_ex"].map(lambda x: f(x, block1))
    df["Block2_ex_stem"] = df["Block2_ex"].map(lambda x: f(x, block2))
    df["Block3_ex_stem"] = df["Block3_ex"].map(lambda x: f(x, block3))
    df["Block4_ex_stem"] = df["Block4_ex"].map(lambda x: f(x, block4))


    def f(x):
        try:
            return nltk.pos_tag([x])[0][1]
        except:
            pass

    # On retrouve le Pos Tag de chaque élément des block ex afin de ne retourner que les noms communs
    df["Block1_ex_pos"] = df["Block1_ex"].map(lambda x: f(x))
    df["Block2_ex_pos"] = df["Block2_ex"].map(lambda x: f(x))
    df["Block3_ex_pos"] = df["Block3_ex"].map(lambda x: f(x))
    df["Block4_ex_pos"] = df["Block4_ex"].map(lambda x: f(x))

    # Variable permettant de dire si les éléments de chaque bloc sont des Noms communs
    df["is_NN"] = df["Block1_ex_pos"].map(lambda x: 1 if x == "NN" else 0)
    df.sort_values(by="is_NN", ascending=False, inplace=True)
    stemmed_nouns = df[["Block1_ex", "Block1_ex_stem"]].groupby("Block1_ex_stem", ).first().reset_index()
    df = df.merge(stemmed_nouns, on="Block1_ex_stem")

    df["is_NN"] = df["Block2_ex_pos"].map(lambda x: 1 if x == "NN" else 0)
    df.sort_values(by="is_NN", ascending=False, inplace=True)
    stemmed_nouns = df[["Block2_ex", "Block2_ex_stem"]].groupby("Block2_ex_stem", ).first().reset_index()
    df = df.merge(stemmed_nouns, on="Block2_ex_stem", how="left")

    df["is_NN"] = df["Block3_ex_pos"].map(lambda x: 1 if x == "NN" else 0)
    df.sort_values(by="is_NN", ascending=False, inplace=True)
    stemmed_nouns = df[["Block3_ex", "Block3_ex_stem"]].groupby("Block3_ex_stem", ).first().reset_index()
    df = df.merge(stemmed_nouns, on="Block3_ex_stem", how="left")

    df["is_NN"] = df["Block4_ex_pos"].map(lambda x: 1 if x == "NN" else 0)
    df.sort_values(by="is_NN", ascending=False, inplace=True)
    stemmed_nouns = df[["Block4_ex", "Block4_ex_stem"]].groupby("Block4_ex_stem", ).first().reset_index()
    df = df.merge(stemmed_nouns, on="Block4_ex_stem", how="left")

    # es.index(index="test", doc_type="test", id=0, body={"test": "test"})
    # id : xxx
    # name_NN : accumulation
    # name_stem : accumulat+
    # block : 1
    # declinaisons : []
    # block1_NN : []
    # block2_NN : []
    # block3_NN : []

    # Pour chaque block :
    for i in range(1, 4):

        block_nb = str(i)
        for item in df["Block" + block_nb + "_ex_y"].dropna().unique():
            filtered = df[df["Block" + block_nb + "_ex_y"] == item]
            dico_to_es = {}
            dico_to_es["name_NN"] = item

            try:
                dico_to_es["name_stem"] = list(filtered["Block" + block_nb + "_ex_stem"])[0]
            except:
                dico_to_es["name_stem"] = ""

            dico_to_es["block"] = str(i)
            dico_to_es["declinaisons"] = list(filtered["Block" + block_nb + "_ex_x"].dropna().unique())
            dico_to_es["block1_NN"] = list(df["Block1_ex_y"].dropna().unique())
            dico_to_es["block2_NN"] = list(df["Block2_ex_y"].dropna().unique())
            dico_to_es["block3_NN"] = list(df["Block3_ex_y"].dropna().unique())
            dico_to_es["block4_NN"] = list(df["Block4_ex_y"].dropna().unique())
            dico_to_es["tab"] = Hkeys[j]
            if i == 3:
                try:
                    dico_to_es["Last_block"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["Last_block"])[0]
                except:
                    pass
                try:
                    dico_to_es["Meaning_H"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["Meaning_H"])[0]
                except:
                    pass
                try:
                    dico_to_es["Patents _nw"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["Patents _nw"])[0]
                except:
                    pass
                try:
                    dico_to_es["Patents_nh"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["Patents_nh"])[0]
                except:
                    pass
                try:
                    dico_to_es["Notions_oc"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["Notions_oc"])[0]
                except:
                    pass

                try:
                    dico_to_es["T&Apli"] = list(df[df["Block3_op"] == dico_to_es["name_stem"]]["T&Apli"])[0]
                except:
                    pass
            print(dico_to_es)
            try:
                es.index(index="peps_heuristiques", doc_type="heur", id=str(id_), body=dico_to_es)
                print("OK !")
            except:
                print('Sthg wrong')
            id_ += 1

            # print(df)
            # print("\n\n ----------------------------------------- \n\n")
"""
