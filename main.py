import flask
from flask import Flask, Blueprint, request, session
from flask_login import login_required, current_user
from flask_cors import CORS
from chemcurate import uniprot_mapping, Chembl, PubChem


main = Blueprint('main', __name__)

display_name_map = {}
organism_display_names = {}
for db in uniprot_mapping.keys():
    display_name_map[db] = {}
    organism_display_names[db] = {}
    for organism_sci_name in uniprot_mapping[db].keys():
        organism_common_name = uniprot_mapping[db][organism_sci_name]['common_name']
        organism_display_name = f'{organism_sci_name} ("{organism_common_name}")' if organism_common_name else organism_sci_name
        organism_display_names[db][organism_display_name] = organism_sci_name
        
        protein_display_names = {}
        for uniprot in uniprot_mapping[db][organism_sci_name]['protein'].keys():
            protein_common_name = uniprot_mapping[db][organism_sci_name]['protein'][uniprot]['common_name']
            protein_display_names[f'{uniprot} ("{protein_common_name}")' if protein_common_name else uniprot] = uniprot
            
        display_name_map[db][organism_display_name] = protein_display_names


def undo_display_protein(organism_protein_map:dict) -> dict:
    '''
    DISPLAY_NAME_MAP
    ----------------
    DB: {
        ORGANISM_DISPLAY_NAME: {
            PROTEIN_DISPLAY_NAME: UNIPROT_ID
        }
    }
    
    ORGANISM_DISPLAY_NAMES
    ----------------------
    DB: {
        ORGANISM_DISPLAY_NAME: ORGANISM_SCI_NAME
    }
    '''
    out = {}
    for db in organism_protein_map.keys():
        out[db] = {}
        out[db]
    out = {}
    for (organism, proteins) in organism_protein_map.items():
        organism_name = organism_display_names[organism]
        protein_names = [protein_display_names[p] for p in proteins]
        out[organism] = []
        for p in protein_names:
            out[organism] += uniprot_mapping[organism_name]['protein'][p]
    return out

@main.route('/get_uniprot_map', methods=['GET'])
def get_uniprot_map() -> dict:
    return display_name_map

@main.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.get_json()
    databases = [d.lower() for d in data['databases']]
    organism_uniprot_map = undo_display_names(data['organism_protein_map'])
    
    try:
        for organism, uniprots in organism_uniprot_map.items():
            if 'pubchem' in databases:
                pubchem = PubChem(uniprots)
                print(pubchem)
            if 'chembl' in databases:
                chembl = Chembl(uniprots)
                
        return '', 204
    
    except Exception as e:
        print(e)
        return {'error': str(e)}, 500

