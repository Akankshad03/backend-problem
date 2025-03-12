import pandas as pd
from typing import List, Dict

def save_to_csv(papers: List[Dict[str, str]], filename: str):
    """Saves paper data to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Results saved to {filename}")
