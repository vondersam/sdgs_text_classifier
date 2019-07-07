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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def extract_num(numbers):
    results = []
    for i in numbers.replace(',', ' ').split():
        if i.lower() not in 'and':
            i = i.strip(punct).split('.')[0]
            if is_number(i) and int(i) in range(1, 18):
                results.append(i)
    return list(set(results))


def format_labels(extracted_goals):
    """
    type_, numbers
    :param extracted_goals: regex-extracted list with type_ and number of labels
    :param numbers:
    :return: list of labels
    """
    labels = []
    for type_, numbers in extracted_goals:
        labels.extend(extract_num(numbers))
    return list(set(labels))


def trans_labels(labels):
    results = dict()
    for i in range(1,18):
        label = f'g_{i}'
        if label in labels:
            results[label] = True
        else:
            results[label] = False
    return results


