#https://textract.readthedocs.io/en/stable/
import os
import json
from utils.document import Document, extract_labels
from utils.extract_utils import trans_labels
import time
import subprocess
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time
from pprint import pprint
import multiprocessing



def download_pdf(file):
    try:
        with open(file, 'rb') as f:
            soup = BeautifulSoup(f, 'html.parser')
            link = soup.find(class_='btn btn-primary library-link')
            if link and 'sdgfund.org_un-promotes-major-regional-agreement-water' not in link:
                link = link['href']
                subprocess.call(['wget', link])
    except:
        print('Did not download')
        print(file)


def extract(filepath, folders=[], spacy_format=False, save=False, format_='dict'):
    start = time.time()
    stats = {}

    output_dir = 'extracted_data/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    labelled = {}
    unlabelled = {}

    for folder in tqdm(folders):
        if folder in os.listdir(filepath):
            folder_files = os.listdir(os.path.join(filepath, folder))

            for f in folder_files:
                time.sleep(1)
                file = os.path.join(folder, f)
                path = os.path.join(filepath + file)
                doc = Document(path, file)
                labelled_data, unlabelled_data = extract_labels(doc)

                if labelled_data:
                    labelled = {**labelled, **labelled_data}
                if unlabelled_data:
                    unlabelled = {**unlabelled, **unlabelled_data}

        stats[folder] = {
            'no_files': len(folder_files),
            'labelled': len(labelled),
            'unlabelled': len(unlabelled),
            'time': time.time() - start,
        }

    pprint(stats)


    if spacy_format:
        final_training = {}
        for k, v in labelled.items():
            final_training[k] = {'cats': trans_labels(v['cats'])}
        labelled = final_training

    if save:
        l_file = output_dir + "labelled"
        u_file = output_dir + "unlabelled"

        if format_ == 'csv':
            pd.DataFrame.from_dict(labelled, orient='index').to_csv(l_file + '.csv')
            pd.DataFrame.from_dict(unlabelled, orient='index').to_csv(u_file + '.csv')

        else:
            with open(l_file + '.json', 'w') as fo:
                json.dump(labelled, fo)
            with open(u_file + '.json', 'w') as fo:
                json.dump(unlabelled, fo)
        total = {
            'no_files': 0,
            'labelled': 0,
            'unlabelled': 0,
            'time': 0,
        }
        for value in stats.values():
            total['no_files'] += value['no_files']
            total['labelled'] += value['labelled']
            total['unlabelled'] += value['unlabelled']
            total['time'] += value['time']
        stats['total'] = total

        with open(output_dir + "stats.json", 'w') as fo:
            json.dump(stats, fo)



main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
#folders = ['word', 'other_html', 'pdf', 'extra_pdf', 'extra_word', 'downloads']
folders = ['pdf']

extract(main_dir, folders, save=True, format_='csv')



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


