import argparse
import requests
from jsonpath_ng import parse, jsonpath

# Define the MyGene.info API endpoint
mygene_api_url = "http://mygene.info/v3/query"

# Function to get gene information by gene symbol
def get_gene_info(symbol):
    # Prepare the URL with the gene symbol as a query parameter
    params = {"q": symbol}

    try:
        # Send a GET request to MyGene.info
        response = requests.get(mygene_api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            gene_info = response.json()
            return gene_info
        else:
            print(f"Error: Unable to retrieve gene information. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

def extract_from_json(json_data,expr):
    jsonpath_expression = parse(expr)
    results = [match.value for match in jsonpath_expression.find(json_data)]
    return results

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Retrieve gene information from MyGene.info")

    # Add a named argument for the gene symbol
    parser.add_argument("--gene-symbol", help="Gene symbol to query", required=True)

    # Parse the command-line arguments
    args = parser.parse_args()

    gene_info = get_gene_info(args.gene_symbol)
    if gene_info:
        print("Gene Information:")
        symbols = extract_from_json(gene_info, '$..symbol')
        print(f"Symbol: {symbols}")
        

