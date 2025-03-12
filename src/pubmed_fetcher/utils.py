from typing import List, Dict

def is_non_academic(affiliation: str) -> bool:
    """Checks if the author is affiliated with a non-academic institution."""
    if not affiliation:
        return False

    non_academic_keywords = ["Inc.", "Ltd.", "Pharma", "Biotech", "Corporation", "Company"]
    return any(keyword in affiliation for keyword in non_academic_keywords)

def filter_non_academic_authors(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filters papers and extracts non-academic authors."""
    filtered_papers = []

    for paper in papers:
        non_academic_authors = [
            author for author in paper["Authors"] if is_non_academic(author["Affiliation"])
        ]

        if non_academic_authors:
            filtered_papers.append({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "PublicationDate": paper["PublicationDate"],
                "NonAcademicAuthors": [author["Name"] for author in non_academic_authors],
                "CompanyAffiliations": [author["Affiliation"] for author in non_academic_authors]
            })

    return filtered_papers
