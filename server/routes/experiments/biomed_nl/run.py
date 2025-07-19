import csv
import time

import requests


def query_and_write_get_to_csv(queries,
                               csv_filename="api_responses.csv",
                               headers=None):
  url = "http://localhost:8080/api/experiments/biomed_nl/query"
  with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["query", "response"])  # Write header row

    for query in queries:
      params = {"q": query}
      print('attemping: ', query)
      start_time = time.time()
      try:
        response = requests.get(url,
                                params=params,
                                headers=headers,
                                timeout=300)
        time_taken = time.time() - start_time
        response.raise_for_status()
        try:
          data = response.json()
          writer.writerow([query, data, time_taken])  # writes the json response
        except requests.exceptions.JSONDecodeError:
          writer.writerow([query, response.text, time_taken
                          ])  # writes raw text in case of non json response.
      except requests.exceptions.Timeout:
        time_taken = time.time() - start_time
        writer.writerow(
            [query, f"Error: Request timed out after 5 min.", time_taken])
        print(f"Request timed out for {query}")
      except requests.exceptions.RequestException as e:
        time_taken = time.time() - start_time
        writer.writerow([query, f"Error: {e}", time_taken])
        print(f"Error querying {query}: {e}")


# Example usage:
queries = [
    "tell me about atorvastatin",
    "What genes are associated with Alzheimer's disease?",
    "Which genetic variants are associated with APOE?",
    "What are genetic variants with the gene symbol KIF6 that are associated with atorvastatin",
    "What can you tell me about atorvastatin",
    "What diseases are associated with the genetic variants associated with atorvastatin",
    "What is the description of atorvastatin?",
    "What is the mechanism of action of atorvastatin",
    "What genetic variants are associated with premature birth?",
    "How many species are there of Chlamydiamicrovirus?",
    "Is there a complete genome for Monkeypox virus?",
    "What is the host of Betapapillomavirus 1?",
    "What is the exemplar isolate of Betapapillomavirus 1?",
    "What is Acanthamoeba polyphaga?",
    "What genes are associated with rs12777823?",
    "What disease is associated with rs7903146?",
    "What genes does rs429358 regulate?",
    "In which tissues is FGFR1 found?",
    "What proteins are associated with FGFR1?",
    "What is the hg38 genomic location of FGFR1?",
    "What are the transcripts of FGFR1?",
    "What type of gene is FGFR1?",
    "What is the HGNC ID of FGFR1?",
    "What diseases is FGFR1 associated with and how are they associated?",
    "What drugs act on FGFR1?",
    "What is the protein level of FGFR1 in macrophages?",
    "What genes are associated with lujo hemorrhagic fever and how were these associations made?",
    "What is the ICD10 code of meningococcal meningitis?",
    "What is the concept unique id for rheumatoid arthritis?",
    "What is the UMLS CUI for rheumatoid arthritis?",
    "What diseases is rheumatoid arthritis associated with?",
    "What is pulmonary embolism a specialization of?",
    "What genes are associated with pulmonary embolism?",
    "What is the chembl ID of acetaminophen?",
    "What is acetaminophen's SMILE?",
    "What drugs are associated with acetaminophen?",
    "What is hydrocortisone a specialization of?",
    "What is the MeSH id for N,N-didesmethyldiltiazem?",
    "What is the pharmacologic action of Diltiazem?",
    "What genes are associated with dopamine?",
    "What genes are associated with dopamine via multilink annotation?",
    "What drugs is rs559628884 associated with?",
    "Are there any drugs that are known to be not associated with rs559628884?",
    "What genetic variants are associated with zonisamide?",
    "What genetic variants are associated with both alzheimer's disease and rheumatoid arthritis?",
    "What genes and genetic variants are associated with atorvastatin?",
    "What proteins are associated with the protein FGFR1?",
]

# queries = [
#     "What genes are associated with Alzheimer's disease?",
#     "What diseases are associated with the genetic variants associated with atorvastatin",
#     "What is the mechanism of action of atorvastatin",
#     "Is there a complete genome for Monkeypox virus?",
#     "What is the exemplar isolate of Betapapillomavirus 1?",
#     "What type of gene is FGFR1?",
#     "What is pulmonary embolism a specialization of?",
#     "Are there any drugs that are known to be not associated with rs559628884?",
#     "What genetic variants are associated with zonisamide?",
# ]
# queries.extend(queries)

query_and_write_get_to_csv(queries)
