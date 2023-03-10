import flask
from flask import Flask, request
from flask_cors import CORS
from chemcurate import uniprot_mapping_filtered


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
        protein_display_names.append('{0} - {1} ({2})'.format(key, protein, ', '.join(uniprot_mapping_filtered[key]['protein'][protein])))
        protein_display_name_mapper[protein_display_names[-1]] = protein
    
    display_name_mapper[organism_display_name] = protein_display_names


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/get_uniprot_map', methods=['GET'])
def get_uniprot_map() -> dict:
    return display_name_mapper

@app.route('/submit', methods=['GET'])
def submit():
    data = request.get_json()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
