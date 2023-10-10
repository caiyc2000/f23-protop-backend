import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Use a service account.
cred = credentials.Certificate('./protop-3bd42-b3a89aad3151.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Make your query & get data from firestore.

