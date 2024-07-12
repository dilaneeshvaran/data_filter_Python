def sort_data(data, sort_key):
    return sorted(data, key=lambda x: x.get(sort_key))
