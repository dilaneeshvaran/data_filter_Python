def filter_data(data, criteria):
    def matches_criteria(item):
        for field, op, value in criteria:
            item_value = item.get(field)
            # Remove commas from the item value if present
            if isinstance(item_value, str):
                item_value = item_value.replace(',', '')

            # Convert the item value and the criteria value to floats for comparison
            try:
                item_value = float(item_value)
                value = float(value)
            except ValueError:
                return False

            if op == '=':
                if item_value != value:
                    return False
            elif op == '>':
                if item_value <= value:
                    return False
            elif op == '<':
                if item_value >= value:
                    return False
        return True

    return [item for item in data if matches_criteria(item)]
