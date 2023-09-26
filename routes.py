from flask import Flask, request
import requests
import json

app = Flask(__name__)


@app.route("/clinvar", methods=["POST"])
def clinvar():
    pdb_id = request.get_json()['pdb_id']

    ids = json.loads(requests.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={pdb_id}[gene]&retmax=500&retmode=json').text)["esearchresult"]["idlist"]

    # https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/
    
    return ids


    
    
@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()