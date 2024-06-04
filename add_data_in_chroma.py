# env =>>>> test2

import psycopg2
import chromadb
from chromadb.utils import embedding_functions
import json
from decimal import Decimal
from InstructorEmbedding import INSTRUCTOR
from chromadb import Documents, EmbeddingFunction, Embeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_key = os.getenv('OPENAI_key')

DATABASE_key = os.getenv('DATABASE_key')
USER_key = os.getenv('USER_key')
PASSWORD_key = os.getenv('PASSWORD_key')
HOST_key = os.getenv('HOST_key')
PORT_key = os.getenv('PORT_key')


arrayCuUnitatiDeMasura = [
    {'fat': 'g'}, {'vitamin_k': 'µg'}, {'copper': 'mg'}, {'vitamin_b5': 'mg'}, {'net_carbohydrates': 'g'}, {'calories': 'kcal'}, {'mono_unsaturated_fat': 'g'}, {'vitamin_a': 'IU'}, {'vitamin_b2': 'mg'}, {'vitamin_b1': 'mg'}, {'vitamin_b3': 'mg'}, {'poly_unsaturated_fat': 'g'}, {'vitamin_e': 'mg'}, {'folic_acid': 'µg'}, {'lycopene': 'µg'}, {'fiber': 'g'}, {'cholesterol': 'mg'}, {'magnesium': 'mg'}, {'folate': 'µg'}, {'vitamin_c': 'mg'}, {'sugar': 'g'}, {'vitamin_d': 'µg'}, {'alcohol': 'g'}, {'choline': 'mg'}, {'saturated_fat': 'g'}, {'vitamin_b6': 'mg'}, {'caffeine': 'mg'}, {'iron': 'mg'}, {'sodium': 'mg'}, {'zinc': 'mg'}, {'vitamin_b12': 'µg'}, {'protein': 'g'}, {'potassium': 'mg'}, {'carbohydrates': 'g'}, {'phosphorus': 'mg'}, {'manganese': 'mg'}, {'selenium': 'µg'}, {'calcium': 'mg'}, {'fluoride': 'mg'}
]

#################################################
#################################################
#################################################
model_emb = INSTRUCTOR('hkunlp/instructor-base')


chroma_client = chromadb.HttpClient(host="localhost", port=8000)

class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:

        sentences = input

        model = INSTRUCTOR('hkunlp/instructor-base')
        arEmb = []
        for prop in sentences:
            embeddings = model.encode([['Represents the name of the food ingredient', prop]])
            arEmb.extend(embeddings)
        # Convert embeddings to a list of lists
        embeddings_as_list = [embedding.tolist() for embedding in arEmb]

        return embeddings_as_list



collection = chroma_client.get_or_create_collection(name="recipes_2", embedding_function=MyEmbeddingFunction())

# print(collection.get())
# print(chroma_client.list_collections())
# # chroma_client.delete_collection(name="recipes")
# quit()
#################################################
#################################################
#################################################



def gasiValoareaDeMasura(nutrient):
    for ob in arrayCuUnitatiDeMasura:
        if nutrient in ob:
            return ob[nutrient]


conn = psycopg2.connect(database=DATABASE_key, user=USER_key,
                        password=PASSWORD_key, host=HOST_key, port=PORT_key)





def scoatemCriptarea(rezultat):
    arNou = []
    for obiect_str in rezultat['documents'][0]:
        ob_nou = obiect_str.replace("\\u00b5g", 'µg')
        arNou.append(ob_nou)
    return arNou


def decimal_to_float(d):
    if isinstance(d, Decimal):
        return float(d)
    return d

def adaugamInChroma(nume, ar_string_nutrienti):
    if len(collection.get()['ids']) < 1:
        try:
            collection.add(
                documents=[nume],
                metadatas=[{"nutrients": ar_string_nutrienti}],
                ids=['1']
            )
        except ZeroDivisionError:
            print('eroare id 1')
    else:
        try:
            collection.add(
                documents=[nume],
                metadatas=[{"nutrients": ar_string_nutrienti}],
                ids=[str(len(collection.get()['ids']) + 1)]
            )
            print('am adaugat cu succes cu id', str(len(collection.get()['ids']) + 1))
        except ZeroDivisionError:
            print('eroare id mai mare ca 1')



pg_client = conn.cursor()

pg_client.execute('select * from valori_nutritionale')
data = pg_client.fetchall()

ar_nume_coloana = [desc[0] for desc in pg_client.description]

for rand in data:
    arNutrienti = []
    nume = rand[len(rand) - 1]
    for nr in range(len(rand)):

        obiect_de_adaugat = { ar_nume_coloana[nr]: decimal_to_float(rand[nr])}
        val = obiect_de_adaugat.keys()
        rezultat = gasiValoareaDeMasura(list(val)[0])
        if rezultat == None : rezultat = ''
        obiect_de_adaugat[ar_nume_coloana[nr]] = str(obiect_de_adaugat[ar_nume_coloana[nr]]) + ' '+ rezultat
        arNutrienti.append(obiect_de_adaugat)



    ar_string_nutrienti = json.dumps(arNutrienti)

    # adaugamInChroma(nume, ar_string_nutrienti)
    ##
    ## pentru a merge cum trebuie acest fisier trebuie sa decomentez chemarea functiei


