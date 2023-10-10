import json
import requests
from config import ROOTDIR
import os

def get_aggregated(pdb_id):
    pdb_results = get_pdb(pdb_id)
    uniprot_results = get_uniprot(pdb_results['uniprot_id'])
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
        print(f'Request failed with status code {response.status_code}')
        return
    
    entry = response.json()['data']['entry']

    id = entry['rcsb_id']
    desc = entry['struct']['title']
    prim_doi = entry['rcsb_primary_citation']['pdbx_database_id_DOI']
    supersedes = [x.get('replace_pdb_id') for x in entry['pdbx_database_PDB_obs_spr']]
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
    pass

def get_knotprot(pdb_id: str) -> dict:
    pass

def get_alphaknot(pdb_id: str) -> dict:
    pass
