# enrich.py

import random
from newspaper import Article

def get_tech_stack(domain):
    tech = ["React", "Node.js", "AWS", "Google Analytics", "Firebase"]
    return random.sample(tech, k=2)

def get_employee_count(domain):
    return random.choice([50, 200, 1000, 5000])

def get_news_snippet(domain):
    try:
        url = f"https://{domain}"
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:150]
    except:
        return "No recent news found."

def enrich_domain(domain):
    return {
        "domain": domain,
        "company_name": domain.split('.')[0].capitalize(),
        "industry": random.choice(["Fintech", "Ecommerce", "Healthcare", "SaaS"]),
        "tech_stack": get_tech_stack(domain),
        "news_snippet": get_news_snippet(domain),
        "employee_count": get_employee_count(domain),
    }
