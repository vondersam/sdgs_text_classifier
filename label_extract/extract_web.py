from bs4 import BeautifulSoup
import os
import json
from string import punctuation
from utils.extract_utils import MAPPINGS
from utils.text import Text


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def extract_type(type_):
    """
    Extract the type of label
    :param type_:
    :return:
    """
    for key, pattern in MAPPINGS.items():
        if type_.lower() in pattern:
            return key

def extract_labels(type_, numbers):
    """
    :param type_:
    :param numbers:
    :return: list of labels
    """
    labels = []
    label_type = extract_type(type_)
    label_numbers = set([i.strip(punctuation) for i in numbers.split() if 'and' not in i])
    for number in label_numbers:
        labels.append(f"{label_type}_{number}")
    return labels



main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/html/'
documents = os.listdir(main_dir)
doc_tracker = {}
training_set = {}
counter = 0


for filename in listdir_nohidden(main_dir):
    numbers = filename.strip('.html')
    file_path = os.path.join(main_dir, filename)
    #counter += 1
    #if counter == 2:
    #    break
    with open(file_path, 'r') as fi:
        page = BeautifulSoup(fi, "html.parser")
        for tag in ['p', 'ul']:
            for entry in page.find_all(tag):
                text = entry.text
                labels = extract_labels('sdg', numbers)
                if "\n\n" in text:
                    texts = [t for t in text.split('\n\n') if t]
                elif " \n" in text:
                    texts = [t for t in text.split(' \n') if t]
                elif ".\n" in text:
                    texts = [t for t in text.split('.\n') if t]
                else:
                    texts = [text]
                for text in texts:
                    text = text.replace('\n', ' ')
                    text = Text(text).text
                    if text:
                        if text not in training_set:
                            training_set[text] = {
                            'cats': labels
                            # 'labels': [],
                            # 'doc_id': document
                            }
                        training_set[text]['cats'].extend(labels)
                        training_set[text]['cats'] = list(set(training_set[text]['cats']))

print(len(training_set))
with open('html_tags.json', 'w') as fo:
    json.dump(training_set, fo)



