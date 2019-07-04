#https://textract.readthedocs.io/en/stable/
import json
from utils.document import Document, extract_labels
from utils.extract_utils import trans_labels
from utils.file_utils import get_files
import time
import subprocess
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time
from multiprocessing import Process, Queue



if __name__ == '__main__':
    start = time.time()
    main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
    folders = ['pdf']
    files = get_files(main_dir, folders)
    final_labelled = {}
    final_unlabelled = {}
    count = 0
    limit = 30

    q = Queue()
    for file in tqdm(files):
        count += 1
        if limit == count:
            break
        doc = Document(main_dir + file)
        p = Process(target=extract_labels, args=(doc, q,))
        p.start()
        labelled, unlabelled = q.get()
        final_labelled = {**final_labelled, **labelled}
        final_unlabelled = {**final_unlabelled, **unlabelled}
        p.join()

    pd.DataFrame.from_dict(final_labelled, orient='index').to_csv('labelled.csv')
    pd.DataFrame.from_dict(final_unlabelled, orient='index').to_csv('unlabelled.csv')
    stats = {
        'labelled': len(final_labelled),
        'unlabelled': len(final_unlabelled)
    }
    with open('stats.json', 'w') as fo:
        json.dump(stats, fo)
    print(time.time()-start)