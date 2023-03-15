import flask
from flask import Flask, Blueprint, request, session
from flask_login import login_required, current_user
from flask_cors import CORS
from chemcurate import uniprot_mapping_filtered, Chembl, PubChem


main = Blueprint('main', __name__)


display_name_mapper = {}
organism_display_name_mapper = {}
protein_display_name_mapper = {}
for key in list(uniprot_mapping_filtered.keys()):
    common_name = uniprot_mapping_filtered[key]['common_name']
    
    organism_display_name = f'{key} ("{common_name}")' if common_name else key
    organism_display_name_mapper[organism_display_name] = key
    
    protein_names = list(uniprot_mapping_filtered[key]['protein'].keys())
    
    protein_display_names = []
    for protein in protein_names:
        protein_display_names.append('{0} ({1})'.format(protein, ', '.join(uniprot_mapping_filtered[key]['protein'][protein])))
        protein_display_name_mapper[protein_display_names[-1]] = protein
    
    display_name_mapper[organism_display_name] = protein_display_names
    

def undo_display_names(organism_protein_map:dict) -> dict:
    out = {}
    for (organism, proteins) in organism_protein_map.items():
        organism_name = organism_display_name_mapper[organism]
        protein_names = [protein_display_name_mapper[p] for p in proteins]
        out[organism] = []
        for p in protein_names:
            out[organism] += uniprot_mapping_filtered[organism_name]['protein'][p]
    return out

@main.route('/get_uniprot_map', methods=['GET'])
def get_uniprot_map() -> dict:
    return display_name_mapper

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

