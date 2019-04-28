from string import punctuation as punct

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


def format_labels(type_, numbers, normalize):
    """
    :param type_:
    :param numbers:
    :return: list of labels
    """
    labels = []
    label_type = extract_type(type_)
    print(numbers)
    label_numbers = set([i.strip(punct) for i in numbers.replace(',', ' ').split() if i.lower() not in 'and'])
    for number in label_numbers:
        if label_type in 'it' and normalize:
            label = f"g_{number.split('.')[0]}"
            labels.append(label)
        else:
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


