## => env test2

from flask import Flask, request, Response
from flask_cors import CORS
import json
from openai import OpenAI
import chromadb
from add_data_in_chroma import MyEmbeddingFunction
from dotenv import load_dotenv
import os

load_dotenv()



OPENAI_key = os.getenv('OPENAI_key')


app = Flask(__name__)
CORS(app)


client = OpenAI(api_key=OPENAI_key)
chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection(name="recipes_2", embedding_function=MyEmbeddingFunction())

def scriemInFisierTxt(ar):
    with open('file_test.txt', 'w') as f:
        for obiect in ar:
            f.write(json.dumps(obiect) +  '\n')



def generatingFunction(completion):
    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content.encode('utf-8')




def makeRequest(istoricMesaje):
    istoricPregatit = []

    for obiect in istoricMesaje:
        if obiect['tip_mesaj'] == 'intrebare' : istoricPregatit.append({"role": "user", "content": obiect['mesaj']})
        if obiect['tip_mesaj'] == 'raspuns': istoricPregatit.append({"role": "assistant", "content": obiect['mesaj']})

    mes = [
        {
            "role": "system",
            "content": '''
                \nTask: You are a chef with artificial intelligence who offers recipes to customers. You are inventive and can create good culinary recipes to help the customer.
                \nAttention: You are ChatGPT, a large language model. Only answer with a recipe if asked for one.
                \nTemplate: Provide your answer in the following format:
                \nName of recipe: [Recipe Name]
                \nIngredients:
                - [Ingredient 1]
                - [Ingredient 2]
                - [Ingredient 3]
                \nInstructions:
                1. [Instruction 1]
                2. [Instruction 2]
                3. [Instruction 3]
                \nBehavior: Ensure the answer is well formatted with clear spaces and lines to make the recipe easy to read.
                \nTechnique: If the task is complex, split it into subtasks. Always run a math check to ensure accurate results.
                \nNote: Pay great attention to formatting. Leave empty lines between sections and ensure the instructions are clear and well-organized.
                '''
        }

    ]

    scriemInFisierTxt(mes + istoricPregatit)

    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:personal::9VcqYlq9",
        messages=mes + istoricPregatit,
        stream=True,
        temperature=0.7,
    )



    # print(completion.choices[0].message.content, '--- il editez ?????')
    return Response(generatingFunction(completion), mimetype = "text/event-stream" )




@app.route("/send_mes" , methods = ['POST'])
def index():
    data = request.json


    rezultat = makeRequest(data['context'])
    return rezultat


##########################################
# <<<<<<<= mesaje
###########################
###########################
###########################
###########################
# =>>>>>>> raport
##########################################

def getDataFromChroma(stringData):
    rezultat = collection.query(
        query_texts=[
            stringData
        ],
        n_results=1)

    return rezultat



def scriemInTxt(ar):
    with open('chroma_results.txt', 'w', encoding='utf-8') as f:
        # print(ar)

        for elem in ar:
            # print('asta e este elem pe care eu il voi scrie in fisier ', elem)
            f.write(elem +  '\n')


def getAlimentFromRecipe(recipe_string):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": '''
                         \nTask: You are an AI bot that removes all foods and ingredients from the recipe, and covert the measures quantity only in grams. 
                         \nAttention: If the quantity doesn t exist, include the food with 0 quantity . 
                         \nTemplate: Provide your answer in JSON structure like this { [food name] : '[x] grams' } 
                         \nBehavior: You will only give me unique foods and aliments with quantity in grams. 
                         \nTechnique: If the task is complex, split it into subtasks. Always run a math check to ensure accurate results. 
                         '''
             },
            {"role": "user",
             "content": recipe_string}
        ],
        response_format={"type": "json_object"}
    )

    return completion.choices[0].message



@app.route("/analyze_recipe" , methods = ['POST'])
def index_doi():
    data = request.json['recipe']

    aliments_list = json.loads(getAlimentFromRecipe(data).content)

    arPtFisierTxt = []
    ar_obDeAlimenteUnice = []

    arDeTrimis = []

    for aliment in aliments_list:
        cantitate = aliments_list[aliment]
        # print(aliment, '---------- >>>>>>>', cantitate)
        rez = getDataFromChroma(aliment)
        # print(rez, '----------- data din chroma')
        nume_aliment_gasit = rez['documents'][0][0]
        print(aliment, '=>>>>>>>', nume_aliment_gasit)
        nutrienti_ar_string = rez['metadatas'][0][0].values()
        nutrienti_ar_string_json = json.dumps(list(nutrienti_ar_string))
        parsed_data = json.loads(nutrienti_ar_string_json)[0].replace("\\u00b5g", 'µg')
        arCuNutrienti = json.loads(parsed_data)

        ob = {}
        if len(ar_obDeAlimenteUnice) == 0:
            ob['name'] = nume_aliment_gasit
            ob['quantity'] = cantitate
            ob['nutrients'] = arCuNutrienti
            # ob[nume_aliment_gasit] = arCuNutrienti
            ar_obDeAlimenteUnice.append(ob)
        else:
            for obiect in ar_obDeAlimenteUnice:
                if obiect['name'] != nume_aliment_gasit:
                    ob['name'] = nume_aliment_gasit
                    ob['quantity'] = cantitate
                    ob['nutrients'] = arCuNutrienti
                    ar_obDeAlimenteUnice.append(ob)

        arDeTrimis.append(ob)
        arPtFisierTxt.append(str(ob))


    scriemInTxt(arPtFisierTxt)


    return arDeTrimis


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)