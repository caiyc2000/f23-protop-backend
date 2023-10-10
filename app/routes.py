from flask import request
import requests
import json
from app import app
from functions.functions import get_aggregated

@app.route('/getProteinData', methods=['GET'])
def get_protein_data():
    pdb_id = request.args.get('pdbID')

    return get_aggregated(pdb_id)
