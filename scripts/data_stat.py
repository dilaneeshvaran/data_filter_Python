import json

def calculate_statistics(data, critere=None):
    if critere:
        champ, operateur, valeur = critere
        if operateur == '=':
            data = [record for record in data if str(record.get(champ)) == str(valeur)]

    champs = {k for d in data for k in d.keys()}
    stats = {champ: {'type': None, 'values': []} for champ in champs}

    for record in data:
        for champ, valeur in record.items():
            if isinstance(valeur, (int, float)) or (isinstance(valeur, str) and valeur.replace('.', '', 1).isdigit()):
                stats[champ]['type'] = 'numeric'
                stats[champ]['values'].append(float(valeur))
            elif isinstance(valeur, bool) or (isinstance(valeur, str) and valeur.lower() in ['true', 'false']):
                stats[champ]['type'] = 'boolean'
                stats[champ]['values'].append(valeur.lower() == 'true' if isinstance(valeur, str) else valeur)
            elif isinstance(valeur, list):
                stats[champ]['type'] = 'list'
                stats[champ]['values'].append(valeur)
            elif isinstance(valeur, str) and ',' in valeur:
                try:
                    list_values = list(map(float, valeur.split(',')))
                    stats[champ]['type'] = 'list'
                    stats[champ]['values'].append(list_values)
                except ValueError:
                    stats[champ]['type'] = 'string'
                    stats[champ]['values'].append(valeur)
            else:
                stats[champ]['type'] = 'string'
                stats[champ]['values'].append(valeur)

    for champ, info in stats.items():
        if info['type'] == 'numeric':
            moyenne = sum(info['values']) / len(info['values'])
            minimum = min(info['values'])
            maximum = max(info['values'])
            info.update({
                'min': minimum,
                'max': maximum,
                'mean': moyenne
            })
        elif info['type'] == 'boolean':
            true_count = sum(1 for v in info['values'] if v is True)
            false_count = len(info['values']) - true_count
            true_percent = (true_count / len(info['values'])) * 100
            false_percent = (false_count / len(info['values'])) * 100
            info.update({
                'true_count': true_count,
                'false_count': false_count,
                'true_percent': true_percent,
                'false_percent': false_percent
            })
        elif info['type'] == 'list':
            flat_values = [item for sublist in info['values'] for item in sublist]
            list_lengths = [len(lst) for lst in info['values']]
            moyenne_length = sum(list_lengths) / len(list_lengths)
            min_length = min(list_lengths)
            max_length = max(list_lengths)
            min_value = min(flat_values)
            max_value = max(flat_values)
            moyenne_value = sum(flat_values) / len(flat_values)
            info.update({
                'min_length': min_length,
                'max_length': max_length,
                'mean_length': moyenne_length,
                'min_value': min_value,
                'max_value': max_value,
                'mean_value': moyenne_value
            })
        elif info['type'] == 'string':
            unique_values = set(info['values'])
            info.update({
                'unique_values': list(unique_values)
            })

    return stats

