# Caprae AI Lead Enrichment Tool

This tool was built for the AI Readiness Challenge by Caprae Capital. It takes in a list of company domains, enriches them with relevant business data, and scores each lead based on sales readiness.

Built using **Streamlit**, this tool combines data enrichment, lead scoring, interactive analytics, and export options into a sleek and professional UI.


## Features

- **AI Enrichment Engine** — Extracts 50+ company attributes from each domain
- **Intelligent Lead Scoring** — Ranks leads 1–100 based on relevance and potential
- **CSV Upload Support** — Input a list of domains via CSV
- **Interactive Dashboard** — Live charts, filters, and metric cards
- **Export Options** — Download your leads in CSV, Excel, or JSON
- **Custom UI** — Fully styled dashboard with responsive layout
- **CRM Ready** — Output structured and formatted for easy import


## Project Structure

```bash
leadgen-ai-tool/
│
├── app.py                 # Main Streamlit app
├── enrich.py              # Enrichment logic per domain
├── score.py               # AI-based lead scoring function
├── requirements.txt       # Dependencies list
├── README.md              # This file
└── sample_data/
    └── leads.csv          # Example input


## How to Run

### Setup
```bash
pip install -r requirements.txt
```

### Run via CLI
```bash
python main.py
```

### Run with UI
```bash
streamlit run app.py
```

## Input Format

`sample_input.csv`
```csv
domain
stripe.com
zoho.com
```

## Output Format

```csv
domain,company_name,industry,tech_stack,news_snippet,employee_count,lead_score
```

## Scoring Logic

Weighted scoring based on:
- Industry match
- Tech stack
- Employee size
- News presence


