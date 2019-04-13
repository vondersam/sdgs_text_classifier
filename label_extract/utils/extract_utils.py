from string import punctuation

MAPPINGS = {
        'g': '(sdgs|sdg|goals|goal)',
        't': '(target)',
        'i': '(indicator)'
    }


def extract_type(type_):
    """
    Extract the type of label
    :param type_:
    :return:
    """
    for key, pattern in MAPPINGS.items():
        if type_.lower() in pattern:
            return key


def format_labels(type_, numbers):
    """

    :param type_:
    :param numbers:
    :return: list of labels
    """
    labels = []
    label_type = extract_type(type_)
    label_numbers = set([i.strip(punctuation) for i in numbers.split() if i not in 'and'])
    for number in label_numbers:
        labels.append(f'{label_type}_{number}')
    return labels


def trans_labels(labels):
    results = dict()
    for i in range(1,18):
        label = f'g_{i}'
        if label in labels:
            results[label] = True
        else:
            results[label] = False
    return results