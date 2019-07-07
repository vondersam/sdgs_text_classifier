import os
import pandas as pd
from bs4 import BeautifulSoup


def download_pdf(file):
    try:
        with open(file, 'rb') as f:
            soup = BeautifulSoup(f, 'html.parser')
            link = soup.find(class_='btn btn-primary library-link')
            if link and 'sdgfund.org_un-promotes-major-regional-agreement-water' not in link:
                link = link['href']
                subprocess.call(['wget', link])
    except:
        print('Did not download')
        print(file)


def get_files(filepath, folders):
    """
    Get all the files from the folders listed given a filepath
    :param filepath:
    :param folders:
    :return:list of files
    """
    files_list = []
    for folder in folders:
        if folder in os.listdir(filepath):
            folder_files = os.listdir(os.path.join(filepath, folder))
            files_list.extend([os.path.join(folder, f) for f in folder_files])
        else:
            print(f'Cannot find {folder} folder in this path.')
    return files_list

def save_files(labelled, unlabelled):
    """
    Save the labelled and unlabelled texts, and stats into .csv and .json formats
    :param labelled:
    :param unlabelled:
    :return: .csv and .json formats
    """
    pd.DataFrame.from_dict(labelled, orient='index').to_csv(
        'labelled.csv')
    pd.DataFrame.from_dict(unlabelled, orient='index').to_csv(
        'unlabelled.csv')

    with open('labelled.json', 'w') as fo:
        json.dump(labelled, fo)
    with open('unlabelled.json', 'w') as fo:
        json.dump(unlabelled, fo)

    stats = {
        'labelled': len(labelled),
        'unlabelled': len(unlabelled)
    }
    with open('stats.json', 'w') as fo:
        json.dump(stats, fo)
