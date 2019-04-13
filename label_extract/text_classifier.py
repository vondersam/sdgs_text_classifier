import spacy
nlp = spacy.load('en_core_web_lg')
import json
import random

# inspired on this
# https://github.com/explosion/spaCy/issues/1997


with open('training_set.json', 'r') as f:
    train_data = json.load(f)
print("Read data...")


textcat = nlp.create_pipe("textcat", config={"exclusive_classes": False})
print("Created pipe...")
nlp.add_pipe(textcat, last=True)
print("starts adding texts...")
for i in range(1,18):
    label = f'g_{i}'
    textcat.add_label(label)
print('finished adding texts')
print('begin training')
optimizer = nlp.begin_training()


for raw_text, labels in train_data.items():
    doc = nlp.make_doc(raw_text)
    gold = GoldParse(doc, cats=labels)
    nlp.update([doc], [gold], drop=0.5, sgd=optimizer)
print('end training')
print('saving model...')
nlp.to_disk('cnn_model')

#print('loading model...')
#nlp = spacy.load('cnn_model')

results = {}
with open('testing.json', 'r') as fi:
  testing = json.load(fi)

  for text,  in testing:
    results[text] = {}
    doc = nlp(text)
    print(doc.cats)
    print()