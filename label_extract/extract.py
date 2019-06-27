#https://textract.readthedocs.io/en/stable/
import os
import json
from utils.document import Document
from utils.file_utils import get_files
from utils.extract_utils import trans_labels
import time
import subprocess
from bs4 import BeautifulSoup
from tqdm import tqdm



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


def extract(filepath, output_filename, folders=[], spacy_format=False, save=False, normalize=False):
    files_list = get_files(filepath, folders)
    data_set = {}
    unlabelled_data_set = {}

    for file in tqdm(files_list):
        path = os.path.join(filepath + file)
        doc = Document(path, file)
        labelled_data, unlabelled_data = doc.extract_labels(normalize)
        if labelled_data:
            data_set = {**data_set, **labelled_data}
        if unlabelled_data:
            unlabelled_data_set = {**unlabelled_data_set, **unlabelled_data}

    if spacy_format:
        final_training = {}
        for k, v in data_set.items():
            final_training[k] = {'cats': trans_labels(v['cats'])}
        data_set = final_training

    if save:
        with open(output_filename + "labelled.json", 'w') as fo:
            json.dump(data_set, fo)
        with open(output_filename + "unlabelled.json", 'w') as fo:
            json.dump(unlabelled_data_set, fo)

    print("Labelled texts:", len(data_set))
    print("Unlabelled texts:", len(unlabelled_data_set))



main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
output_filename = 'filtered_millenium'
#folders = ['word', 'other_html', 'pdf', 'extra_pdf', 'extra_word', 'downloads']
folders = ['word']

start = time.time()
extract(main_dir, output_filename, folders, save=True, normalize=True)
end = time.time()
print(end - start)


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


