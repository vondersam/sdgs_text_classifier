import json

def to_binary(file):
    with open(file, 'r') as fi:
        data = json.load(fi)
        for text in data:
            pass