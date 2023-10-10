from functions.functions import get_pdb
from functions.utils import get_uniprot_from_pdb

print(get_pdb("4HHB"))

print(get_uniprot_from_pdb(get_pdb("4HHB"), "A"))