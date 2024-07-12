def filter_data(data, criteria):
    def matches_criteria(item):
        for field, value in criteria.items():
            if item.get(field) != value:
                return False
        return True
    
    return [item for item in data if matches_criteria(item)]
