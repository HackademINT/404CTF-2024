import numpy as np


def seek(search_key, search_value, data):
    return next((item for item in data if item.get(search_key) == search_value), None)


def weights_from_dict(data: dict):
    return [np.array(data[k]) for k in data.keys()]
