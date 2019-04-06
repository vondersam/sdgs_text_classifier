#https://textract.readthedocs.io/en/stable/
import textract

from io import BytesIO
from lxml import etree

from docx import Document
import docx
import subprocess
import re
import os
import json
from string import punctuation



class Text():
    def __init__(self, t):
        self.text = t


class DocDocument:
    def __init__(self, extracted_string):
        self.paragraphs = []
        # Decode and split by paragraphs
        extracted_list = extracted_string.decode('utf-8').split('\n\n')
        for line in extracted_list:
            # Eliminate extra spaces, replace space characters and eliminate break lines
            processed_text = re.sub(' +', ' ', line.strip().replace('\xa0', ' ').replace('\n', ' '))
            self.paragraphs.append(Text(processed_text))


def extract_type(type_):
    for key, pattern in mappings.items():
        if type_.lower() in pattern:
            return key


def extract_labels(type_, numbers):
    labels = []
    label_type = extract_type(type_)
    label_numbers = set([i.strip(punctuation) for i in numbers.split() if 'and' not in i])
    for number in label_numbers:
        labels.append(f'{label_type}_{number}')
    return labels


main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/word/'
documents = os.listdir(main_dir)
doc_tracker = {}

training_set = {}
target = '/Users/samuelrodriguezmedina/Google Drive/Language Technology/thesis/datasets/SDGs_articles/wpf'

mappings = {
    'g': 'SDG|goals|goal',
    't': 'target',
    'i': 'indicator'
}



for document in documents:
    path = os.path.join(main_dir + document)
    doc = None
    try:
        # Docx
        doc = Document(path)
    except:
        try:
            # Doc
            extracted = subprocess.check_output(['antiword', '-t', path])
            doc = DocDocument(extracted)
        except Exception as e:
            print(e)

    if doc:
        for paragraph in doc.paragraphs:
            text = paragraph.text
            # To avoid extracting Millennium Goals
            if 'millennium' not in text.lower():
                patterns = [
                    f"({mappings['g']})\s+([,*\s*\d+]+[and]*[\s+\d+]*)",
                    f"({mappings['t']})(\s+\d+\.[\d+a-d])",
                    f"({mappings['i']})(\s+\d+\.[\d+a-d]\.\d+)"
                ]
                for pattern in patterns:
                    goals = re.findall(pattern, text, re.I)
                    for type_, numbers in goals:
                        if numbers:
                            labels = extract_labels(type_, numbers)
                            if labels:
                                if text not in training_set:
                                    training_set[text] = {
                                        'labels': [],
                                        'doc_id': document
                                    }
                                training_set[text]['labels'].extend(labels)
                                training_set[text]['labels'] = list(set(training_set[text]['labels']))
                                if document not in doc_tracker:
                                    doc_tracker[document] = []
                                doc_tracker[document].extend(labels)


# Track documents with one
for doc, labels in doc_tracker.items():
    if len(set(labels)) == 1:
        print(doc, labels)

# Save results to file

#with open('training_set.json', 'w') as fo:
#    json.dump(training_set, fo)
#print(len(training_set))



'''
- if one label happens more than once, should they be weighted? Or maybe just use a set, do not repeat labels
- if only one label is mentioned in a document, label all paragraphs as that label
-indicators refer to targets, and targets to goals, but this does not work the other way around
- check what happens with text in track changes
- Goals are to be found in texts about Millenium Development Goals. Should we include them?
- Still get Millennium goals if the word millennium is not present in the paragraph
- try to eliminate text with all the labels, since they're ambiguous
- should labels happening more than once be more weighted?
- E_CN.17_2007_14 -> goal 10 years later

'''





