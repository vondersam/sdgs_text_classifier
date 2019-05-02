import os

def get_files(filepath, folders):
    """
    Get all the files from the folders listed given a filepath
    :param filepath:
    :param folders:
    :return:
    """
    files_list = []
    for folder in folders:
        if folder in os.listdir(filepath):
            folder_files = os.listdir(os.path.join(filepath, folder))
            files_list.extend([os.path.join(folder, f) for f in folder_files])
        else:
            print(f'Cannot find {folder} folder in this path.')
    return files_list
