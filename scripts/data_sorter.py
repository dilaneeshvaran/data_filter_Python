def sort_data(data, sort_key):
    def get_sort_value(item):
        value = item
        for key in sort_key.split('.'):
            if isinstance(value, dict):
                value = value.get(key, None)
            if value is None:
                return 0
            
        if isinstance(value, str):
            value = value.replace(',', '') 
            try:
                value = float(value)
            except ValueError:
                return 0

        return value

    return sorted(data, key=lambda x: get_sort_value(x), reverse=True) 
