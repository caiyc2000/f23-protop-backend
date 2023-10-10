from flask import request
import requests
import json
from app import app
from functions.functions import get_aggregated

@app.route('/getResults', methods=['GET'])
def get_results():
    pdb_id = request.args.get('pdbID')

    return get_aggregated(pdb_id)
