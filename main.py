import flask
from flask import Flask, Blueprint, request, session
from flask_login import login_required, current_user
from flask_cors import CORS
# from autochem import uniprot_mapping
# from autochem.api_client import Chembl, PubChem
from autochem import PubChemQuery
from collections import defaultdict
from typing import List, Dict
import pandas as pd
from copy import deepcopy
import naclo
from io import BytesIO


main = Blueprint('main', __name__)

# display_name_map = {}
# protein_display_names_2_uniprot = {}
# organism_display_names = {}

# for db in uniprot_mapping.keys():
#     display_name_map[db] = {}
#     organism_display_names[db] = {}
#     for organism_sci_name in uniprot_mapping[db].keys():
#         organism_common_name = uniprot_mapping[db][organism_sci_name]['common_name']
#         organism_display_name = f'{organism_sci_name} ("{organism_common_name}")' if organism_common_name else organism_sci_name
#         organism_display_names[db][organism_display_name] = organism_sci_name
        
#         protein_display_names = {}
#         for uniprot in uniprot_mapping[db][organism_sci_name]['protein'].keys():
#             protein_common_name = uniprot_mapping[db][organism_sci_name]['protein'][uniprot]['common_name']
#             protein_display_name = f'{uniprot} ("{protein_common_name}")' if protein_common_name else uniprot
#             protein_display_names[protein_display_name] = uniprot
#             protein_display_names_2_uniprot[protein_display_name] = uniprot
            
#         display_name_map[db][organism_display_name] = protein_display_names

pubchem_query = PubChemQuery()
pubchem_organism_uniprot_df = pubchem_query.get_organism_data_for_all_pubchem_uniprot_ids()


# def display_names_2_uniprot_ids(db:str, organism_protein_map:dict) -> List[str]:
#     '''
#     DISPLAY_NAME_MAP
#     ----------------
#     DB: {
#         ORGANISM_DISPLAY_NAME: {
#             PROTEIN_DISPLAY_NAME: UNIPROT_ID
#         }
#     }
    
#     ORGANISM_DISPLAY_NAMES
#     ----------------------
#     DB: {
#         ORGANISM_DISPLAY_NAME: ORGANISM_SCI_NAME
#     }
#     '''
#     return [display_name_map[db][organism][p]
#             for (organism, proteins) in organism_protein_map.items()
#             for p in proteins]

# @main.route('/get_uniprot_map', methods=['GET'])
# def get_uniprot_map() -> dict:
#     return display_name_map

def all_formatted_organism_names_map() -> Dict[str, str]:
    formatted_names_map = {}
    for _, row in pubchem_organism_uniprot_df.iterrows():
        formatted_name = f'{row["organism_sci_name"]} ("{row["organism_common_name"]}")' if \
            row["organism_common_name"] else row["organism_sci_name"]
            
        if formatted_name not in formatted_names_map: # filter duplicates
            formatted_names_map[formatted_name] = row['organism_sci_name']
    return formatted_names_map

def subset_formatted_protein_names_map(organism_map:Dict[str, str]) -> Dict[str, str]:
    organism_protein_map = {}
    
    for formatted_name, sci_name in organism_map.items():
        organism_protein_map[formatted_name] = {}
        
        subset_df = pubchem_organism_uniprot_df.where(pubchem_organism_uniprot_df['organism_sci_name'] == sci_name).dropna()
        
        for _, row in subset_df.iterrows():
            formatted_protein_name = f'{row["uniprot_id"]} ("{row["protein_name"]}")' if row["protein_name"] else row["uniprot_id"]
            
            if formatted_protein_name not in organism_protein_map[formatted_name]:
                organism_protein_map[formatted_name][formatted_protein_name] = row['uniprot_id']
    
    return organism_protein_map
            
    
    
    

@main.route('/get_organism_names', methods=['GET'])
@login_required
def get_organism_names() -> List[str]:
    return all_formatted_organism_names_map()

@main.route('/post_protein_names', methods=['POST'])
def post_protein_names():
    organism_map = request.get_json()['organism_map']
    return subset_formatted_protein_names_map(organism_map)

@main.route('/submit_uniprot_query', methods=['POST'])
@login_required
def submit_uniprot_query():
    uniprot_ids = request.get_json()['uniprot_ids']
    
    dfs = [pubchem_query.get_bioassays_from_uniprot_id(uniprot_id) for uniprot_id in uniprot_ids]
    
    big_df = pd.concat(dfs)
    
    buf = BytesIO()
    writer = naclo.dataframes.Writer(big_df, mol_col_name='ROMol')
    buf = writer.write(out=buf, ext='csv')
    
    return flask.send_file(buf, as_attachment=True, download_name='autochem_out.csv')

@main.route('/get_all_protein_accessions', methods=['GET'])
@login_required
def get_all_protein_accessions():
    out = pubchem_query.get_protein_accessions_with_data()
    return out

@main.route('/submit_protein_accession_query', methods=['POST'])
@login_required
def submit_protein_accession_query():
    protein_accessions = request.get_json()['protein_accessions']
    
    dfs = [pubchem_query.get_bioassays_from_protein_accession(protein_accession) for protein_accession in protein_accessions]
    big_df = pd.concat(dfs)
    
    buf = BytesIO()
    writer = naclo.dataframes.Writer(big_df, mol_col_name='ROMol')
    buf = writer.write(out=buf, ext='csv')
    
    return flask.send_file(buf, as_attachment=True, download_name='autochem_out.csv')

    
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

