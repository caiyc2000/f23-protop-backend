import json
import requests
from config import ROOTDIR
import os
import itertools

def get_aggregated(pdb_id):
    pdb_results = get_pdb(pdb_id)
    
    if pdb_results.get('error'):
        return {'error': f'Please check your PDB ID: {pdb_results["error"]}'}

    uniprot_results = [get_uniprot(uniprot_id) for entity in pdb_results.get('entities') for uniprot_id in entity.get('uniprot_ids')]
    knotprot_results = get_knotprot(pdb_id)
    alphaknot_results = get_alphaknot(pdb_id)

    return json.dumps({
        'pdb': pdb_results,
        'uniprot': uniprot_results,
        'knotprot': knotprot_results,
        'alphaknot': alphaknot_results
    })

def get_pdb(pdb_id: str) -> dict:

    with open(os.path.join(ROOTDIR, 'functions/graphql/pdb.graphql'), 'r') as f:
        query = f.read()

    variables = {
        "id": pdb_id
    }

    response = requests.post('https://data.rcsb.org/graphql', json={'query': query, 'variables': json.dumps(variables)})

    if response.status_code != 200:
        return {'error': f'Request failed with status code {response.status_code}'}
        
    entry = response.json()['data']['entry']

    id = entry['rcsb_id']
    desc = entry['struct']['title']
    prim_doi = entry['rcsb_primary_citation']['pdbx_database_id_DOI']
    supersedes = [x.get('replace_pdb_id') for x in entry['pdbx_database_PDB_obs_spr']] if entry['pdbx_database_PDB_obs_spr'] else []
    keywords = entry['struct_keywords']['pdbx_keywords']
    organisms = list(set([organism['scientific_name'] for entity in entry['polymer_entities'] for organism in entity['rcsb_entity_source_organism']]))
    mutations = sum([entity['entity_poly']['rcsb_mutation_count'] for entity in entry['polymer_entities']])
    deposited = entry['rcsb_accession_info']['deposit_date']
    released = entry['rcsb_accession_info']['initial_release_date']
    authors = entry['citation'][0]['rcsb_authors']

    method = entry['refine'][0]['pdbx_refine_id']
    resolution = entry['refine'][0]['ls_d_res_high']
    rvalue = entry['refine'][0]['ls_R_factor_R_work']


    entities = []
    for entity in entry['polymer_entities']:
        molecule = entity['rcsb_polymer_entity']['pdbx_description']
        chains = entity['rcsb_polymer_entity_container_identifiers']['asym_ids']
        auth_chains = entity['rcsb_polymer_entity_container_identifiers']['auth_asym_ids']
        length = entity['entity_poly']['rcsb_sample_sequence_length']
        organism = entity['rcsb_entity_source_organism'][0]['scientific_name']
        mutations = entity['entity_poly']['rcsb_mutation_count']
        primary_data_genes = [gene.get('value') for gene in entity['rcsb_entity_source_organism'][0]['rcsb_gene_name'] if gene.get('provenance_source') == "Primary Data"]
        uniprot_genes = [gene.get('value') for gene in entity['rcsb_entity_source_organism'][0]['rcsb_gene_name'] if gene.get('provenance_source') == "Uniprot"]
        uniprot_ids = entity['rcsb_polymer_entity_container_identifiers']['uniprot_ids']

        entities.append({
        'molecule': molecule,
        'chains': chains,
        'auth_chains': auth_chains,
        'length': length,
        'organism': organism,
        'mutations': mutations,
        'primary_data_genes': primary_data_genes,
        'uniprot_genes': uniprot_genes,
        'uniprot_ids': uniprot_ids,
        })

    return {
        'id': id,
        'desc': desc,
        'prim_doi': prim_doi,
        'supersedes': supersedes,
        'keywords': keywords,
        'organisms': organisms,
        'mutations': mutations,
        'deposited': deposited,
        'released': released,
        'authors': authors,
        'method': method,
        'resolution': resolution,
        'rvalue': rvalue,
        'entities': entities
    }


def get_uniprot(uniprot_id: str) -> dict:
    
    # UniProt API URL
    api_url = f"https://rest.uniprot.org/uniprot/{uniprot_id}.json"

    # Send a GET request to UniProt
    response = requests.get(api_url)

    # Check the response status
    if response.status_code != 200:
        return{"Error": f"{response.status_code} - Unable to retrieve UniProt data"}
   
    # Store the response
    response = response.json()

    # Extract information from the JSON response
    protein_name = response['proteinDescription']['recommendedName']['fullName']['value']
    gene_name= response['genes'][0]["geneName"]["value"]
    ec = [keyword.get("name") for keyword in response["keywords"] if keyword.get("id") == "KW-0378"]
    sequence = response['sequence']['value']
    length = response['sequence']['length']
    organism = response['organism']['scientificName']
    diseases = [
        {
            'diseaseId': entry["disease"]["diseaseId"],
            'xRef': entry["disease"]["diseaseCrossReference"],
        } for entry in response["comments"] if "disease" in entry]

    #variants #Getting this is challenging, as the response does not show the natural variants under each disease involvement, instead, it shows all natural variants in "feature" list. Some natural variants in this list have no pathological significance.

    # Need to use the variants api for this
    variants_api = f"https://www.ebi.ac.uk/proteins/api/variation?offset=0&size=100&accession={uniprot_id}"

    # Send a GET request to UniProt Variants API
    response = requests.get(variants_api)

    if response.status_code != 200:
        return{"Error": f"{response.status_code} - Unable to retrieve UniProt data"}
   
    response = response.json()
    
    disease_associated_variants = (feature for feature in response[0]['features'] if feature.get('association'))

    variants_by_disease = {disease.get('diseaseId'): [] for disease in diseases} # Initialize
    for variant in disease_associated_variants:
        for disease in diseases:
            diseaseId = disease['diseaseId']
            diseaseRef = disease['xRef']
            for association in variant.get('association'):
                for associationRef in association.get('dbReferences', []):
                    if diseaseRef['database'] == associationRef['name'] and diseaseRef['id'] == associationRef['id']:
                        variants_by_disease[diseaseId].append({
                            'begin': variant['begin'],
                            'end': variant['end'],
                            'wildType': variant['wildType'],
                            'mutatedType': variant.get('mutatedType')
                        })

    # return as a dictionary
    return {
        'id': uniprot_id,
        'protein': protein_name,
        'gene': gene_name,
        'emzyme_classification': ec,
        'organism': organism,
        'sequence': sequence,
        'length': length,
        'diseases': diseases,
        'variants': variants_by_disease
    }

def get_knotprot(pdb_id: str) -> dict:
    pass

def get_alphaknot(pdb_id: str) -> dict:
    pass
