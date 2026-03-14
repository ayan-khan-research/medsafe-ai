def parse_csv_text(value):
    return [item.strip() for item in value.split(',')] if value else []


def safe_badge(level):
    color = {
        'Low Risk': '#16a34a',
        'Medium Risk': '#d97706',
        'High Risk': '#dc2626',
    }.get(level, '#334155')
    return f"<div style='padding:10px;border-radius:10px;background:{color};color:white;font-weight:600;display:inline-block'>{level}</div>"
