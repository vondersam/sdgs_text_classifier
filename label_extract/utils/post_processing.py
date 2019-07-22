import csv
import re
import json
import pandas as pd
from langdetect import detect
from tqdm import tqdm
from multiprocessing import Process, Queue
import sys
import csv
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


"""
with open('new_labelled.csv', 'r') as one, open('labelled_filenamelabel.csv', 'r') as two:
    new_labelled = csv.DictReader(one, strict=False)
    latest = csv.DictReader(two, strict=False)
    latest_dict = {row['text']: {'cats': row['cats'], 'doc_id': row['doc_id']} for row in latest}


    with open("final.csv", "w") as fo:
            fieldnames = ['text', 'cats', 'doc_id']
            writer = csv.DictWriter(fo, fieldnames=fieldnames)

            writer.writeheader()
            for row in new_labelled:
                if row['text'] in latest_dict:
                    writer.writerow({
                        'text': row['text'],
                        'cats': latest_dict[row['text']]['cats'],
                        'doc_id': row['doc_id']
                        })

with open('previous.csv', 'r') as one:
    previous = csv.DictReader(one, strict=False)
    pattern = r'^(\w{1} )([A-Z])'

    with open("final.csv", "w") as fo:
            fieldnames = ['text', 'cats', 'doc_id']
            writer = csv.DictWriter(fo, fieldnames=fieldnames)

            for row in previous:
                text = row['text']
                if re.search(pattern, row['text']):
                    text = re.sub(pattern, "\g<2>", text)
                writer.writerow({
                        'text': text,
                        'cats': row['cats'],
                        'doc_id': row['doc_id']
                        })



with open('html_tags.json', 'r') as f:
    data = json.load(f)
    final = {}
    for text, values in data.items():
        final[text] = {'cats': [values['cats'][0].strip('g_')]}

    df = pd.DataFrame.from_dict(final, columns=["text", "cats"], orient="index")
    df.to_csv("html.csv")
"""

def detect_lang(text, q=None):
    if q:
        try:
            q.put((detect(text[:150]), text))
        except:
            q.put(('de', ""))
    else:
        try:
            return detect(text), text
        except:
            return 'de', ""

if __name__ == '__main__':

    with open('from_pandas.csv', 'r') as f:
        data = csv.DictReader(f, strict=False)

        with open("cleanup_unlabelled_final.csv", "w") as fo:
            fieldnames = ['text']
            writer = csv.DictWriter(fo, fieldnames=fieldnames)
            writer.writeheader()
            #q = Queue()

            for row in tqdm(data):
                try:
                    #p = Process(target=detect_lang, args=(row['text'],q))
                    #p.start()
                    #language, text = q.get()
                    language, text = detect_lang(row['text'])
                    if language == "en":
                        writer.writerow({'text': text})
                    #p.join()
                except:
                    pass

