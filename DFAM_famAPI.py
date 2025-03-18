import requests
import argparse

# parser
parser = argparse.ArgumentParser(description='DFAM API wrapper')
parser.add_argument('-q', '--query', type = str, metavar='<family_nane>', help='family name substring to search', dest = 'query')
parser.add_argument('-Q', '--query_list', type = str, metavar='<list_of_family_nane>', help='list of family name substring to search in a file', dest = 'query')
parser.add_argument('-t', '--taxid', type = str, metavar='<ncbi_tax_id>', help='ncbi taxon id', dest = 'taxid')
parser.add_argument('-l', '--limit', type = str, metavar='<max_responses>', help='maximum number of response per query', dest = 'limit', default = "10")
parser.add_argument('-m', '--mode', type = str, metavar='<tool_mode>', help='type of request', dest = 'mode', default = "find_accession")
args = parser.parse_args()

# functions

################################
# Match name with DF accession #
################################
# This function need a list of TE name in the query file and return matching DF entries (and names)

def match_name_to_accession():
    for fname in open(args.query):
    #    print(fname)
        url = "https://dfam.org/api/families"
        params = {
            # The summary format is metadata-only and does not include
            # full details such as the consensus sequence and citations
            "format": "summary",
            # Only retrieve the first 10 results in this query
            "limit": args.limit,
            # Search clade (ncbi tax_id)
            "clade": args.taxid,
            # Include families from ancestor and descendant taxa in the results
            "clade_relatives": "both",
            # Search specific name
            "name": fname.strip()
            }
    #    print(params)
        # fetch the results
        response = requests.get(url, params=params)
        results = response.json()["results"]
        # get the number of matches
        response_len=response.json()["total_count"]

        #print the names matching the query
        for i in range(response_len):
            print(fname.strip() + "\t" + results[i]['name'] + "\t" + results[i]['accession'])

########################
# Get consensus length #
########################
# This function returns the length of each consensus for a given taxid

def return_consensus_length():
    url = "https://dfam.org/api/families"
    params = {
    # The summary format is metadata-only and does not include
    # full details such as the consensus sequence and citations
    "format": "summary",
    # Only retrieve the first 10 results in this query
    #"limit": args.limit,
    # Search clade (ncbi tax_id)
    "clade": args.taxid,
    # Include families from ancestor and descendant taxa in the results
    "clade_relatives": "both",
    # Search specific name
    #"name": fname.strip()
    }
    #    print(params)
    # fetch the results
    response = requests.get(url, params=params)
    results = response.json()["results"]
    # get the number of matches
    response_len=response.json()["total_count"]
    #print(results)
    for i in range(response_len):
        try:
            subtype = "/" + results[i]['repeat_subtype_name']
        except KeyError:
            subtype = ""
        print(results[i]['accession'] + "\t" + results[i]['name'] + "\t" + results[i]['repeat_type_name'] + subtype + "\t" + str(results[i]['length']))


# workflow

if args.mode == "find_accession":
    match_name_to_accession()
elif args.mode == "cons_len":
    return_consensus_length()

