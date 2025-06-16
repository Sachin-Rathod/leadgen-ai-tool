# score.py

def score_lead(row):
    score = 50

    if 'Fintech' in row.get('industry', ''):
        score += 15
    if row.get('employee_count') and int(row['employee_count']) > 1000:
        score += 10
    if 'AWS' in row.get('tech_stack', []):
        score += 10
    if row.get('news_snippet'):
        score += 5

    return min(score, 100)
