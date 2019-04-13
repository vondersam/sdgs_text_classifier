#https://textract.readthedocs.io/en/stable/
import re
import os
import json
from utils.document_utils import Document
from utils.file_utils import get_files



def extract(filepath, output_filename, folders=[], spacy_format=False, save=False):
    files_list = get_files(filepath, folders)
    data_set = {}

    for file in files_list:
        path = os.path.join(filepath + file)
        doc = Document(path)
        labelled_data = doc.extract_labels()
        if labelled_data:
            data_set = {**data_set, **labelled_data}

    if spacy_format:
        """
        final_training = {}
        for k, v in data_set.items():
            final_training[k] = {'cats': trans_labels(v['cats'])}
        """

        # Track documents with one
        # for doc, labels in doc_tracker.items():
        #    if len(set(labels)) == 1:
        #        print(doc, labels)
    if save:
        with open(output_filename, 'w') as fo:
            json.dump(data_set, fo)
        print(len(data_set))


main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
output_filename = 'working.json'
folders = ['word', 'other_html', 'pdf']
extract(main_dir, output_filename, folders, save=True)





