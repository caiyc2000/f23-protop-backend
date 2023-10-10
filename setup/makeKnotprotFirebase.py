import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Use a service account.
cred = credentials.Certificate('./protop-3bd42-b3a89aad3151.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

with open('./knotdata.csv', 'r') as f:
    data = pd.read_csv(f, delimiter=';')

for _, row in data.iterrows():
    newDocument = {
        'pdb_id': row['# PDB code'],
        'chain': row['Chain'],
        'chainLength': row['Chain Length'],
        'category': row['{Y,A,T}={Published,Artifact,Not published}'],
        'knotCategory': row['{K,S}={Knot,Slipknot}'],
        'knotType': row['Main knot type (e.g. 31=3.1)'],
        'nCut': row['N_cut'],
        'cCut': row['C_cut'],
        'knotRangeStart': row['Knots range'].split('-')[0],
        'knotRangeEnd': row['Knots range'].split('-')[1]
    }
    
    print(db.collection('knotprot').add(newDocument))

    