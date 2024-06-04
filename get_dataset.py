## env =>> test2


from openai import OpenAI
from datasets import load_dataset
import json
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_key = os.getenv('OPENAI_key')



client_ai = OpenAI(api_key=OPENAI_key)


dataset = load_dataset("TigerResearch/tigerbot-kaggle-recipes-en-2k")
train = dataset['train']

## contine doua mii de retete!!!!



def create_line(questions, answer):
    return {
        "messages": [
            {"role": "system", "content": 'You are a cook who knows recipes for cooking.'},
            {"role": "user", "answer": answer},
            {"role": "assistant", "questions": questions},
        ]
    }



def create_questions(text):
    messages = [
        {'role': 'system', 'content': 'You are a recipe book that receives a recipe and you have to formulate questions based on it. " \
            "The questions should be formulated so that you can understand the recipe. "\
            "Converts bodies of text into a single question.'
         },
        {'role': 'user', 'content': 'Text: ' + text}
    ]
    response = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=3,
        temperature=0.7,
    )
    response_text = response.choices

    arCuIntrebari = []

    for pozitie in range(len(response_text)):
        if len(arCuIntrebari) > 4 : return arCuIntrebari
        arCuIntrebari.append(response_text[pozitie].message.content)

    # print(arCuIntrebari)
    return arCuIntrebari



## --------------------------------------------------------


n = 0
for rand in train:

    n += 1

    if n > 500  and n <= 1000 :

        with open("train_data.jsonl", "a", encoding="utf-8") as f:
            numele_retetei = rand['input']
            reteta = rand['output'].replace('\n', ' ')
            ingrediente = reteta[:reteta.index('instructions')]
            metoda_de_preparare = reteta[reteta.index('instructions'):]

            text_reteta = 'name: '+ numele_retetei+ '. ' +ingrediente+ '. ' +metoda_de_preparare

            intrebari_string = ', '.join(create_questions(text_reteta))
            print(intrebari_string, '\n', '----------------------------------------------------------------')

            example_str = json.dumps(create_line(intrebari_string, text_reteta), ensure_ascii=False)
            f.write(example_str + '\n')

    elif n <= 500: continue
    else : break


