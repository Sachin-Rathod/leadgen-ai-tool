# main.py

import pandas as pd
from enrich import enrich_domain
from score import score_lead
from tqdm import tqdm

def main():
    df = pd.read_csv("sample_input.csv")
    results = []

    for domain in tqdm(df['domain']):
        enriched = enrich_domain(domain)
        enriched['lead_score'] = score_lead(enriched)
        results.append(enriched)

    pd.DataFrame(results).to_csv("sample_output.csv", index=False)
    print("✅ Done! Output saved to sample_output.csv")

if __name__ == "__main__":
    main()
