import json
from utils.document import Document, extract_labels, merge_dicts
from utils.file_utils import get_files, save_files
import time
from tqdm import tqdm
from multiprocessing import Process, Queue



if __name__ == '__main__':
    start = time.time()
    # Indicate the path to the files from where the texts
    # and labels need to be extracted.
    main_dir = '/Users/samuelrodriguezmedina/Documents/ir4sdgs/crawl_sdgs/'
    folders = [
        'word',
        'other_html',
        'pdf',
        'extra_pdf',
        'extra_word',
        'downloads',
        'downloadable_pdfs'
    ]
    files = get_files(main_dir, folders)
    final_labelled = {}
    final_unlabelled = {}
    q = Queue()

    for file in tqdm(files):
        p = Process(target=extract_labels, args=(doc, q,))
        p.start()
        labelled, unlabelled = q.get()
        if labelled:
            final_labelled = merge_dicts(final_labelled, labelled)
        if unlabelled:
            final_unlabelled = {**final_unlabelled, **unlabelled}
        p.join()

    save_files(final_labelled, final_unlabelled)
    print(time.time()-start)
