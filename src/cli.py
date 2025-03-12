import argparse
from src.pubmed_fetcher.fetcher import PubMedFetcher
from src.pubmed_fetcher.utils import filter_non_academic_authors
from src.pubmed_fetcher.exporter import save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    
    args = parser.parse_args()

    fetcher = PubMedFetcher(email="your-email@example.com")

    print(f"Fetching papers for query: {args.query}...")
    paper_ids = fetcher.fetch_paper_ids(args.query)
    papers = fetcher.fetch_paper_details(paper_ids)
    filtered_papers = filter_non_academic_authors(papers)

    if args.file:
        save_to_csv(filtered_papers, args.file)
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()
