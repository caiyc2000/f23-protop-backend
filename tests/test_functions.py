from functions.functions import get_pdb, get_uniprot
from functions.utils import get_uniprot_from_pdb
import json

pdb_dict = get_pdb("4HHB")
print(json.dumps(pdb_dict, indent=4))

uniprot_dict = get_uniprot_from_pdb(pdb_dict, "A")
print(json.dumps(uniprot_dict, indent=4))

uniprot_info = get_uniprot('Q92560')
print(json.dumps(uniprot_info, indent=4))
