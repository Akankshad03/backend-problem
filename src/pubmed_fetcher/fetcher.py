import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

class PubMedFetcher:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, email: str):
        self.email = email

    def fetch_paper_ids(self, query: str, max_results: int = 10) -> List[str]:
        """Fetches paper IDs from PubMed using a given query."""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "xml",
            "email": self.email
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        return [id_elem.text for id_elem in root.findall(".//Id")]

    def fetch_paper_details(self, paper_ids: List[str]) -> List[Dict[str, str]]:
        """Fetches paper details given a list of PubMed IDs."""
        if not paper_ids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(paper_ids),
            "retmode": "xml",
            "email": self.email
        }
        response = requests.get(self.DETAILS_URL, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        papers = []

        for article in root.findall(".//PubmedArticle"):
            paper_data = {
                "PubmedID": article.findtext(".//PMID"),
                "Title": article.findtext(".//ArticleTitle"),
                "PublicationDate": article.findtext(".//PubDate/Year"),
                "Authors": self.extract_authors(article)
            }
            papers.append(paper_data)

        return papers

    def extract_authors(self, article) -> List[Dict[str, str]]:
        """Extract authors and affiliations from a PubMed article."""
        authors = []
        for author in article.findall(".//Author"):
            last_name = author.findtext("LastName", "")
            first_name = author.findtext("ForeName", "")
            affiliation = author.findtext(".//Affiliation", "")

            authors.append({
                "Name": f"{first_name} {last_name}".strip(),
                "Affiliation": affiliation
            })
        return authors
