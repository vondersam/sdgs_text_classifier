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
#folders = ['word', 'other_html', 'pdf']
folders = ['word']
extract(main_dir, output_filename, folders, save=True)

'''
- we need to do more processing:
    - delete numbered bullet points starting a paragraph
    - delete noisy symbols such as bar |
    - what should we do with the numbers, label them? <number>
- if one label happens more than once, should they be weighted? Or maybe just use a set, do not repeat labels
- if only one label is mentioned in a document, label all paragraphs as that label
-indicators refer to targets, and targets to goals, but this does not work the other way around
- check what happens with text in track changes
- Goals are to be found in texts about Millenium Development Goals. Should we include them?
- Still get Millennium goals if the word millennium is not present in the paragraph
- try to eliminate text with all the labels, since they're ambiguous
- should labels happening more than once be more weighted?
- E_CN.17_2007_14 -> goal 10 years later
- scraping 'https://sustainabledevelopment.un.org/sdg10'
- evaluate the very simple classifier that we have
'''





