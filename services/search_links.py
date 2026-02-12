from urllib.parse import quote_plus

def encode_query(query: str) -> str:
    return quote_plus(query)
