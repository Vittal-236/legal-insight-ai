def parse_nlu_response(response, filename):
    """
    Parses the JSON response from Watson NLU into a flat dictionary
    based on the project's output schema.
    """
    
    # 1. Extract Entities (People, Orgs, Laws)
    # We combine text and type for clarity, e.g., "Section 420 IPC (Law)"
    entities = []
    for e in response.get('entities', []):
        text = e.get('text', 'N/A')
        etype = e.get('type', 'Unknown')
        # Filter for common relevant types, add more as needed
        if etype in ['Person', 'Organization', 'Location', 'Law', 'LegalReference', 'GovernmentAgency']:
             entities.append(f"{text} ({etype})")
    
    # 2. Extract Categories
    categories = [c.get('label', 'N/A') for c in response.get('categories', [])]
    
    # 3. Extract Document Sentiment
    sentiment = "neutral" # Default
    doc_sentiment = response.get('sentiment', {}).get('document', {})
    if doc_sentiment:
        sentiment = doc_sentiment.get('label', 'neutral')

    # 4. Extract Keywords
    keywords = [k.get('text', 'N/A') for k in response.get('keywords', [])]

    # 5. Build the final structured dictionary
    structured_output = {
        "file": filename,
        "entities": ", ".join(sorted(list(set(entities)))), # Use set to remove duplicates
        "categories": ", ".join(sorted(list(set(categories)))),
        "sentiment": sentiment,
        "keywords": ", ".join(sorted(list(set(keywords))))
    }
    
    return structured_output