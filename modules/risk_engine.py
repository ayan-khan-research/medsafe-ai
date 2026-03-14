
def calculate_risk_score(medicines, symptoms, allergies, med_db, interaction_result):
    symptoms = [s.lower().strip() for s in symptoms if s.strip()]
    allergies = [a.lower().strip() for a in allergies if a.strip()]

    score = 0
    breakdown = {
        'interaction_points': 0,
        'side_effect_points': 0,
        'allergy_points': 0,
        'polypharmacy_points': 0,
    }
    matched_side_effects = []

    if interaction_result['warnings']:
        severe_found = any(w['severity'] == 'high' for w in interaction_result['warnings'])
        breakdown['interaction_points'] = 40 if severe_found else 25
        score += breakdown['interaction_points']

    for med in medicines:
        info = med_db.get(med, {})
        med_side_effects = [x.lower() for x in info.get('side_effects', [])]
        matches = sorted(set(symptoms).intersection(med_side_effects))
        if matches:
            breakdown['side_effect_points'] += min(25, 10 + 5 * len(matches))
            matched_side_effects.append({'medicine': med, 'matches': matches})

        contraindications = [x.lower() for x in info.get('avoid_if', [])]
        allergy_matches = sorted(set(allergies).intersection(contraindications + [med]))
        if allergy_matches:
            breakdown['allergy_points'] += 30

    score += breakdown['side_effect_points']
    score += breakdown['allergy_points']

    if len(medicines) > 3:
        breakdown['polypharmacy_points'] = 10
        score += 10

    return {
        'score': min(score, 100),
        'breakdown': breakdown,
        'matched_side_effects': matched_side_effects,
    }


def risk_level(score):
    if score >= 60:
        return 'High Risk'
    if score >= 30:
        return 'Medium Risk'
    return 'Low Risk'


def build_recommendations(score_breakdown, interaction_result):
    score = score_breakdown['score']
    recs = []
    if interaction_result['warnings']:
        recs.append('Review the detected interaction pair before taking the medicines together.')
    if score_breakdown['matched_side_effects']:
        recs.append('Some entered symptoms overlap with known side effects in the demo database.')
    if score >= 60:
        recs.append('High-risk result: consult a doctor or pharmacist urgently before proceeding.')
    elif score >= 30:
        recs.append('Medium-risk result: verify dosage, history, and possible interactions with a professional.')
    else:
        recs.append('Low-risk result in demo logic, but still verify with a healthcare professional.')
    recs.append('This result is educational only and not a medical prescription.')
    return recs
