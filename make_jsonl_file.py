## env =>>>> test2
import json
import pandas as pd
import jsonlines


DEFAULT_SYSTEM_PROMPT = 'You are a cook who knows recipes for cooking.'

def create_dataset(question, answer):
    return {
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
    }


with jsonlines.open('train_data.jsonl') as f:
    with open("train_data_doi.jsonl", "w") as file:
        for line in f.iter():
            intrebari_string = line['messages'][2]['question']
            reteta_string = line['messages'][1]['answer']
            example_str = json.dumps(create_dataset(intrebari_string, reteta_string))
            file.write(example_str + "\n")



# if __name__ == "__main__":
#     df = pd.read_csv("./training_data.csv")
#     with open("train_data.jsonl", "w") as f:
#         for _, row in df.iterrows():
#             rand  = row['text']
#             indexUnu = rand.index('human')
#             indexDoi = rand.index('bot')
#             human = rand[indexUnu: indexDoi]
#             bot = rand[indexDoi:]
#            # sciem in fiesierul jsonl
#             example_str = json.dumps(create_dataset(bot, human))
#             # f.write(example_str + "\n")

