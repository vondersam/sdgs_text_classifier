import json
import csv

def get_dict(text, tags):
    result = {
    'g_1': 0,
    'g_2': 0,
    'g_3': 0,
    'g_4': 0,
    'g_5': 0,
    'g_6': 0,
    'g_7': 0,
    'g_8': 0,
    'g_9': 0,
    'g_10': 0,
    'g_11': 0,
    'g_12': 0,
    'g_13': 0,
    'g_14': 0,
    'g_15': 0,
    'g_16': 0,
    'g_17': 0
    }
    result['text'] = text
    for tag in tags:
        try:
            result[tag] = 1
        except:
            pass
    return result


def to_binary(file):
    with open(file, 'r') as fi:
        data = json.load(fi)
        fieldnames = ['text',
                      'g_1',
                      'g_2',
                      'g_3',
                      'g_4',
                      'g_5',
                      'g_6',
                      'g_7',
                      'g_8',
                      'g_9',
                      'g_10',
                      'g_11',
                      'g_12',
                      'g_13',
                      'g_14',
                      'g_15',
                      'g_16',
                      'g_17']

        with open('final_final.csv', 'w') as fo:
            writer = csv.DictWriter(fo, fieldnames=fieldnames)
            writer.writeheader()

            for text, tags in data.items():
                d = get_dict(text, tags['cats'])
                writer.writerow(d)


path = '../label_extract/final_final.json'
to_binary(path)