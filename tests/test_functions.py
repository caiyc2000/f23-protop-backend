from functions.functions import get_pdb, get_uniprot
from functions.utils import get_uniprot_from_pdb
import json

pdb_dict = get_pdb("1A3N")
print(json.dumps(pdb_dict, indent=4))

#uniprot_info = get_uniprot('Q92560')
#print(json.dumps(uniprot_info['variants'], indent=4))

# for disease, mutants in uniprot_info['variants'].items():
#     for mutant in mutants:
#         if mutant['begin'] != mutant['end']:
#             print(disease, mutant)


