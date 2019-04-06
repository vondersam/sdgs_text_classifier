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

main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/word/'
documents = os.listdir(main_dir)

training_set = {}
target = '/Users/samuelrodriguezmedina/Google Drive/Language Technology/thesis/datasets/SDGs_articles/wpf'


class Text():
    def __init__(self, t):
        self.text = t


class DocDocument:
    def __init__(self, extracted_string):
        self.paragraphs = []
        extracted_list = extracted_string.decode('utf-8').split('\n\n')
        for line in extracted_list:
            processed_text = re.sub(' +', ' ', line.strip().replace('\xa0', ' ').replace('\n', ''))
            self.paragraphs.append(Text(processed_text))


for document in documents:
    path = os.path.join(main_dir + document)
    doc = None
    try:
        # Use docx
        doc = Document(path)
    except:
        try:
            extracted = subprocess.check_output(['antiword', '-t', path])
            doc = DocDocument(extracted)
        except Exception as e:
            print(e)

    if doc:
        for paragraph in doc.paragraphs:
            text = paragraph.text
            goal_pattern = '(SDG|goal)\s?(\d+)'
            target_pattern = '(target)\s?(\d+)'
            indicator_pattern = ''

            goals = re.findall(goal_pattern, text, re.I)
            if goals:
                for goal in goals:
                    goal_label = f'g_{goal[1]}'
                    if text not in training_set:
                        training_set[text] = {
                            'labels': [],
                            'doc_id': document
                        }
                    if goal_label not in training_set[text]:
                        training_set[text]['labels'].append(goal_label)



'''
- if one label happens more than once, should they be weighted? Or maybe just use a set, do not repeat labels
- if only one label is mentioned in a document, label all paragraphs as that label
-indicators refer to targets, and targets to goals, but this does not work the other way around
- try without 'target', 'goal', and see what results you get: (target)\s\d+(\.\d+)*
- check what happens with text in track changes
'''


with open('training_set.json', 'w') as fo:
    json.dump(training_set, fo)
print(len(training_set))



