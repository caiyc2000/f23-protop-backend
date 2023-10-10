import json
import requests

def get_aggregated(pdb_id):
    pdb_results = get_pdb(pdb_id)
    uniprot_results = get_uniprot(pdb_results['uniprot_id'])
    knotprot_results = get_knotprot(pdb_id)
    alphaknot_results = get_alphaknot(pdb_id)

    # Aggregate Logic

def get_pdb(pdb_id: str) -> dict:

    with open('./graphql/pdb.graphql', 'r') as f:
        query = f.read()

    variables = {
        "id": "4HHB"
    }

    response = requests.post('https://data.rcsb.org/graphql', json={'query': query, 'variables': json.dumps(variables)})

    if response.status_code == 200:
        data = response.json()['data']
        # Do something with the data
    else:
        print(f'Request failed with status code {response.status_code}')

    return data

def get_uniprot(uniprot_id: str) -> dict:
    pass

def get_knotprot(pdb_id: str) -> dict:
    pass

def get_alphaknot(pdb_id: str) -> dict:
    pass
