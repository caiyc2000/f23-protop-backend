from flask import request
import json
from app import app
from functions.functions import get_aggregated

@app.route('/getProteinData', methods=['GET'])
def get_protein_data():
    pdb_id = request.args.get('pdbID')
    
    if not pdb_id:
        return json.dumps({"Error": "No PDB ID provided. Please pass via the pdbID parameter."}), 400
    
    return get_aggregated(pdb_id)