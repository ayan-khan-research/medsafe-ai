from itertools import combinations


def normalize_medicine_list(items):
    return sorted({item.strip().lower() for item in items if item and item.strip()})


def check_medicine_safety(medicines, med_db):
    warnings = []
    known = []
    unknown = []

    for med in medicines:
        info = med_db.get(med)
        if info:
            known.append({
                'medicine': med,
                'category': info.get('category', 'unknown'),
                'common_use': info.get('use', 'N/A'),
                'common_side_effects': ', '.join(info.get('side_effects', [])),
            })
        else:
            unknown.append(med)

    for a, b in combinations(medicines, 2):
        a_info = med_db.get(a, {})
        pair_key = '|'.join(sorted([a, b]))
        interaction = a_info.get('interactions', {}).get(pair_key)
        if interaction:
            warnings.append({
                'pair': f'{a} + {b}',
                'severity': interaction.get('severity', 'medium'),
                'message': interaction.get('message', 'Potential interaction detected'),
            })

    return {
        'warnings': warnings,
        'known_medicines': known,
        'unknown_medicines': unknown,
    }
