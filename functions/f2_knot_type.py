import os
import pandas as pd

def get_knot_type_catalog():
    ROOTDIR = os.path.dirname(os.path.realpath(__file__))
    ak_dataset_path = os.path.join(ROOTDIR, '../Datasets/alphaknot_knots_dataset.txt')
    knotprot_path = os.path.join(ROOTDIR, '../Datasets/knotprot_dataset.txt')
    alphaknot_ds = pd.read_csv(ak_dataset_path, sep='\t', header=None)
    knotprot_ds = pd.read_csv(knotprot_path, sep=';', header=None)
    alphaknot_catalog = pd.DataFrame(columns=['Knot_type', 'Source', 'ID'])
    knotprot_catalog = pd.DataFrame(columns=['Knot_type', 'Source', 'ID'])
    for idx, data in alphaknot_ds.iterrows():
        if idx:
            alphaknot_catalog.loc[len(alphaknot_catalog.index)] = [data[0], 'AlphaKnot', data[2]]
    alphaknot_catalog.sort_values('Knot_type', inplace=True)
    for idx, data in knotprot_ds.iterrows():
        if data[4] == 'K' and data[3] == 'Y':
            if idx and isinstance(data[5], str):
                if len(data[5]) == 2:
                    knotprot_catalog.loc[len(knotprot_catalog.index)] = [data[5][0] + '_' + data[5][1], 'KnotProt', data[0]]
    knotprot_catalog.sort_values('Knot_type', inplace=True)

    frames = [alphaknot_catalog, knotprot_catalog]
    knot_type_catalog = pd.concat(frames)
    knot_type_catalog.sort_values('Knot_type', inplace=True)
    return knot_type_catalog, alphaknot_catalog, knotprot_catalog

knot_type_catalog, alphaknot_catalog, knotprot_catalog = get_knot_type_catalog()
print(knotprot_catalog)
