#https://textract.readthedocs.io/en/stable/
import os
import json
from utils.document_utils import Document
from utils.file_utils import get_files
from utils.extract_utils import trans_labels
import time
import nltk


def extract(filepath, output_filename, folders=[], spacy_format=False, save=False, normalize=False):
    files_list = get_files(filepath, folders)
    data_set = {}

    for file in files_list:
        path = os.path.join(filepath + file)
        doc = Document(path)
        labelled_data = doc.extract_labels(normalize)
        if labelled_data:
            data_set = {**data_set, **labelled_data}

    if spacy_format:
        final_training = {}
        for k, v in data_set.items():
            final_training[k] = {'cats': trans_labels(v['cats'])}
        data_set = final_training

    if save:
        with open(output_filename, 'w') as fo:
            json.dump(data_set, fo)
    print(len(data_set))


main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
output_filename = 'final_final.json'
#folders = ['word', 'other_html', 'pdf']
folders = ['txt']

#start = time.time()
#extract(main_dir, output_filename, folders, save=True, normalize=True)
#end = time.time()
#print(end - start)


result = extract(main_dir, output_filename, folders, save=True, normalize=True)
print(result)


"""
tokens = []
for name in ['final_final.json']:
    with open(name, 'r') as f:
        data = json.load(f)
        print(f'Number of entries in {name}:', len(data))
        for text in data:
            tokens.extend(nltk.word_tokenize(text))
    print(len(tokens))
    print(len(set(tokens)))
"""


