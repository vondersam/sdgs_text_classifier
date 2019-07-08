#https://textract.readthedocs.io/en/stable/
import json
from utils.document import Document, extract_labels, merge_dicts
from utils.file_utils import get_files, save_files
import time
import subprocess
#https://textract.readthedocs.io/en/stable/
from tqdm import tqdm
import time
from multiprocessing import Process, Queue
import re



if __name__ == '__main__':
    start = time.time()
    main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
    folders = ['word', 'other_html', 'pdf', 'extra_pdf', 'extra_word', 'downloads', 'downloadable_pdfs']
    files = get_files(main_dir, folders)
    final_labelled = {}
    final_unlabelled = {}
    q = Queue()
    pattern =  r'(goal-)((?:[1-9]\b|1[0-7]?\b))'

    for file in tqdm(files):
        match = re.search(pattern, file, flags=re.IGNORECASE)
        if match:
            print(file)
            doc = Document(main_dir + file, filename=file)
            p = Process(target=extract_labels, args=(doc, q,))
            p.start()
            labelled, unlabelled = q.get()
            final_labelled = merge_dicts(final_labelled, labelled)
            final_unlabelled = merge_dicts(final_unlabelled, unlabelled)
            #final_labelled = {**final_labelled, **labelled}
            #final_unlabelled = {**final_unlabelled, **unlabelled}
            p.join()

    save_files(final_labelled, final_unlabelled)
    print(time.time()-start)
