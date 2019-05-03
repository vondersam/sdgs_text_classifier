from string import punctuation as punct

MAPPINGS = {
        'g': r'(sdgs|sdg|goals|goal)',
        't': r'(target)',
        'i': r'(indicator)'
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


def extract_num(numbers):
    results = []
    for i in numbers.replace(',', ' ').split():
        if i.lower() not in 'and':
            i = i.strip(punct).split('.')[0]
            if int(i) in range(1, 19):
                results.append(i)
    return set(results)


def format_labels(type_, numbers, normalize):
    """
    :param type_:
    :param numbers:
    :return: list of labels
    """
    labels = []
    label_type = extract_type(type_)
    #label_numbers = set([i.strip(punct) for i in numbers.replace(',', ' ').split() if i.lower() not in 'and'])
    label_numbers = extract_num(numbers)
    print(label_numbers)
    for number in label_numbers:
        # Use goals only, instead of indices and targets
        label = f"g_{number}"
        labels.append(label)
        # Use goals, indices and targets
        #else:
        #    labels.append(f'{label_type}_{number}')
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


