import flask
from flask import Flask, Blueprint, request, session
from flask_login import login_required, current_user
from flask_cors import CORS
from chemcurate import uniprot_mapping, Chembl, PubChem
from collections import defaultdict
from typing import List


main = Blueprint('main', __name__)

display_name_map = {}
protein_display_names_2_uniprot = {}
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
            protein_display_name = f'{uniprot} ("{protein_common_name}")' if protein_common_name else uniprot
            protein_display_names[protein_display_name] = uniprot
            protein_display_names_2_uniprot[protein_display_name] = uniprot
            
        display_name_map[db][organism_display_name] = protein_display_names


def display_names_2_uniprot_ids(db:str, organism_protein_map:dict) -> List[str]:
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
    return [display_name_map[db][organism][p]
            for (organism, proteins) in organism_protein_map.items()
            for p in proteins]

@main.route('/get_uniprot_map', methods=['GET'])
def get_uniprot_map() -> dict:
    return display_name_map

@main.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.get_json()
    database = data['databases'].lower()
    uniprot_ids = display_names_2_uniprot_ids(database, data['organism_protein_map'])
    
    if database == 'chembl':
        out = Chembl(uniprot_ids)
        print(out)
    
    elif database == 'pubchem':
        PubChem(uniprot_ids)
        # pass
    
    return '', 204
    # organism_uniprot_map = undo_display_names(data['organism_protein_map'])
    
    # try:
    #     for organism, uniprots in organism_uniprot_map.items():
    #         if 'pubchem' in databases:
    #             pubchem = PubChem(uniprots)
    #             print(pubchem)
    #         if 'chembl' in databases:
    #             chembl = Chembl(uniprots)
                
    #     return '', 204
    
    # except Exception as e:
    #     print(e)
    #     return {'error': str(e)}, 500

