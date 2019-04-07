import spacy
nlp = spacy.load('en_core_web_lg')
import json

# inspired on this
# https://github.com/explosion/spaCy/issues/1997

'''
train_data = [
    (u"That was very bad", {"cats": {"POSITIVE": 0, "NEGATIVE": 1}}),
    (u"it is so bad", {"cats": {"POSITIVE": 0, "NEGATIVE": 1}}),
    (u"so terrible", {"cats": {"POSITIVE": 0, "NEGATIVE": 1}}),
    (u"I like it", {"cats": {"POSITIVE": 1, "NEGATIVE": 0}}),
    (u"It is very good.", {"cats": {"POSITIVE": 1, "NEGATIVE": 0}}),
    (u"That was great!", {"cats": {"POSITIVE": 1, "NEGATIVE": 0}})
]
'''

with open('training_set.json', 'r') as f:
    data = json.load(f)
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


for doc, gold in data.items():
    nlp.update([doc], [gold], sgd=optimizer)
print('end training')
samples = {
    "88.\tThe Office of the High Representative for the Least Developed Countries, Landlocked Developing Countries and Small Island Developing States also convened a meeting in November 2015 on enhancing the coherence of small island developing States issues in United Nations processes following the adoption of the Samoa Pathway and in the context of the 2030 Sustainable Development Agenda. The meeting allowed an initial mapping of the United Nations processes relating to small island developing States and addressed the need to have small island developing States focal points at the national level with direct linkages to the global processes to ensure the coherence of small island developing States issues at the global and national levels (Sustainable Development Goal 17).": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  },
  "89.\tThe World Bank Group has recently established a new small States secretariat. The secretariat is responsible for the annual Small States Forum, which is held during the annual meetings of the World Bank and the International Monetary Fund to discuss the implications of the emerging development architecture for small States (Sustainable Development Goal 17).": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  },
  "90.\tThe United Nations system continues to be active at the country level. In the Africa, Indian Ocean, Mediterranean and South China Sea regions, UNFPA has worked with the Government of the Comoros, for instance, on the United Nations Development Assistance Framework for the period 2015-2019 in tandem with the Government\u2019s Strategy for Accelerated Growth and Sustainable Development 20152019. In the Caribbean and the Pacific, UNFPA also supported the efforts of Governments, in implementing household and population censuses, to collect data to inform development programmes (Sustainable Development Goals 8 and 17). UNICEF country offices contributed to the development of the next five-year multicountry sustainable development framework. The activities and priorities of the framework are based, in part, on the Samoa Pathway and enable the United Nations to work as a whole in a coordinated manner to address issues of climate change and environmental sustainability (Sustainable Development Goals 8, 13, 15 and 17).": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 1,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 1,
      "g_14": 0,
      "g_15": 1,
      "g_16": 0,
      "g_17": 1
    }
  },
  "92.\tJamaica has continued to implement Vision 2030 Jamaica, its sustainable development plan. Since the adoption of the Samoa Pathway, Jamaica has approved a medium-term socioeconomic policy framework for 2015-2018. The framework incorporates most of the thematic areas of the Samoa Pathway and is aligned to country strategies and programmes of international development partners (Sustainable Development Goal 17).": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  },
  "93.\tSamoa conducted a preliminary integrated assessment to create a Sustainable Development Goals profile, which involved a broad consultative process in conjunction with the midterm review of its national development strategy and the subsequent development of a new strategy (2016-2020). Samoa has integrated the priorities of the Samoa Pathway into the new strategy for 2016-2020, which has the theme \u201cAccelerating sustainable development and creating opportunities for all\u201d. Work is already in progress to tailor implementation of the Sustainable Development Goals and targets to the Samoan context and a national task force is in place for that purpose (Sustainable Development Goal 17). As noted above, Samoa was the first small island developing State to undertake a national voluntary review at the high-level political forum on sustainable development.": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  },
  "94.\tSingapore undertakes regular policy reviews, planning for the long term, yet retaining the flexibility to review plans as needed. A multi-agency team regularly collects data on the 18 indicators identified in the Sustainable Singapore Blueprint 2015 to monitor progress towards 2030 targets for expanding green and blue spaces, increasing transport mobility, improving resource sustainability, enhancing air quality, improving drainage systems and encouraging community stewardship in sustainable development. In addition, Singapore regularly updates the Blueprint, which maps out strategies to meet the country\u2019s unique challenges. The 2015 Blueprint charts the next steps towards building \u201ceco-smart\u201d towns, reducing reliance on private car transportation, achieving a zero-waste society, developing a leading green economy and fostering an active and gracious community. This will all contribute to the implementation of the 2030 Agenda (Sustainable Development Goals 1, 3, 8, 11, 12, 15 and 17).": {
    "cats": {
      "g_1": 1,
      "g_2": 0,
      "g_3": 1,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 1,
      "g_9": 0,
      "g_10": 0,
      "g_11": 1,
      "g_12": 1,
      "g_13": 0,
      "g_14": 0,
      "g_15": 1,
      "g_16": 0,
      "g_17": 1
    }
  },
  "95.\tThe Dominican Republic has created a high-level commission on sustainable development, which aims to promote the formulation of policies, programmes and projects and the coordination of national efforts for the realization of sustainable development in the public and private sectors. The commission is responsible for implementing and creating linkages between international frameworks on sustainable development, including the 2030 Agenda, and the national planning system (Sustainable Development Goal 17). ": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  },
  "96.\tAt the regional level, ESCAP has supported national sustainable development strategies through integrated planning, including linking national planning priorities to budgetary processes and fiscal policies. Key initiatives include a partnership with the International Monetary Fund Pacific Financial Technical Assistance Centre to assist members in integrating sustainable development into their fiscal policies, and support for the preparation and review of national sustainable development strategies in the Pacific (Sustainable Development Goal 17).": {
    "cats": {
      "g_1": 0,
      "g_2": 0,
      "g_3": 0,
      "g_4": 0,
      "g_5": 0,
      "g_6": 0,
      "g_7": 0,
      "g_8": 0,
      "g_9": 0,
      "g_10": 0,
      "g_11": 0,
      "g_12": 0,
      "g_13": 0,
      "g_14": 0,
      "g_15": 0,
      "g_16": 0,
      "g_17": 1
    }
  }
}

for text in samples:
    print(text)
    doc = nlp(text)
    print(doc.cats)