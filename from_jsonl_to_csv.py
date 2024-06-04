## env =>>>>>> test2

import json
import csv
import jsonlines

with open('training_data.csv', 'a', encoding='utf-8') as file_w:
    writer = csv.writer(file_w)
    column_names = ['text']
    writer.writerow(column_names)

    with jsonlines.open('train_data.jsonl') as f:

        for line in f.iter():
            intrebari_string = line['messages'][2]['question']
            reteta_string = line['messages'][1]['answer']
            # print(line['messages'][1]['answer'] , '--------------------------------', '\n')
            pair_str = 'answer: ' + reteta_string + ' \n questions: ' + intrebari_string

            writer.writerow([pair_str])