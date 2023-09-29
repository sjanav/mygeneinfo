import argparse
import requests

# Define the MyGene.info API endpoint for single queries
single_query_url = "http://mygene.info/v3/query"

# Define the MyGene.info API endpoint for batch queries
batch_query_url = "http://mygene.info/v3/query"

# Function to get gene information by gene symbol for single queries
def single_query_gene_info(symbol):
    params = {
        "q": symbol,
        "fields": "symbol,name,entrezgene",
        "fetch_all": False  # Ensure only one result is returned for single query
    }

    try:
        response = requests.get(single_query_url, params=params)

        if response.status_code == 200:
            gene_info = response.json()
            return gene_info['hits'][0] if 'hits' in gene_info and len(gene_info['hits']) > 0 else None
        else:
            print(f"Error: Unable to retrieve gene information. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Function to perform a batch query
def batch_query_gene_info(gene_symbols):
    params = {
        "q": ",".join(gene_symbols),
        "scopes": "symbol",
        "fields": "name,symbol,entrezgene",
    }

    try:
        response = requests.post(batch_query_url, data=params)

        if response.status_code == 200:
            gene_info_list = response.json()
            return gene_info_list
        else:
            print(f"Error: Unable to retrieve gene information. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# Define subcommand functions
def single_query_command(args):
    if args.gene_symbol:
        gene_info = single_query_gene_info(args.gene_symbol)
        if gene_info:
            print("Gene Information:")
            entrezgene_id = gene_info.get('entrezgene', 'EntrezGene ID not available')
            print(f"EntrezGene ID: {entrezgene_id}")
            gene_name = gene_info.get('name', 'Name not available')
            print(f"Name: {gene_name}")
            symbol = gene_info.get('symbol', 'Symbol not available')
            print(f"Symbol: {symbol}")
    else:
        print("Error: For single queries, you must specify a gene symbol.")

def batch_query_command(args):
    if args.text_file:
        try:
            with open(args.text_file, "r") as text_file:
                gene_symbols = [line.strip() for line in text_file if line.strip()]
                gene_info_list = batch_query_gene_info(gene_symbols)
                if gene_info_list:
                    for gene_info in gene_info_list:
                        print(f"Symbol: {gene_info.get('symbol', 'Symbol not available')}")
                        print(f"Name: {gene_info.get('name', 'Name not available')}")
                        print(f"EntrezGene ID: {gene_info.get('entrezgene', 'EntrezGene ID not available')}")
                        print()
        except FileNotFoundError:
            print(f"Error: The specified TXT file '{args.text_file}' does not exist.")
        except Exception as e:
            print(f"Error processing TXT file: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve gene information from MyGene.info")

    # Create a subparsers object to handle subcommands
    subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand", description="Available subcommands")

    # Subcommand for single query
    single_query_parser = subparsers.add_parser("single", help="Perform a single gene query")
    single_query_parser.add_argument("--gene-symbol", help="Gene symbol to query")
    single_query_parser.set_defaults(func=single_query_command)

    # Subcommand for batch query
    batch_query_parser = subparsers.add_parser("batch", help="Perform a batch gene query")
    batch_query_parser.add_argument("-t", "--text-file", help="Path to a txt file containing gene symbols")
    batch_query_parser.set_defaults(func=batch_query_command)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
