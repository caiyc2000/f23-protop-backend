def get_uniprot_from_pdb(pdb_response, chain):
    """
    Takes response from functions/functions/get_pdb and a chain ID and returns the uniprot ID for that chain

    pdb_response: dict
    chain: str
    """

    for entity in pdb_response['entities']:
        if chain in entity['chains']:
            return entity['uniprot_ids']

    return []
    