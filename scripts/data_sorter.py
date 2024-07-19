def sort_data(data, sort_keys):
    def get_sort_value(item, key):
        value = item
        for k in key.split('.'):
            if isinstance(value, dict):
                value = value.get(k, None)
            if value is None:
                return float('-inf')

        if isinstance(value, str):
            value = value.replace(',', '')
            try:
                value = float(value)
            except ValueError:
                pass

        return value

    if isinstance(sort_keys, str):
        sort_keys = [sort_keys]

    return sorted(data, key=lambda x: [get_sort_value(x, key) for key in sort_keys], reverse=True)
