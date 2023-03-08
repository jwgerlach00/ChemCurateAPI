import flask
from flask import Flask, request
from flask_cors import CORS
from chemcurate import uniprot_mapping_filtered


display_name_mapper = {}
display_names = []
for key in list(uniprot_mapping_filtered.keys()):
    common_name = uniprot_mapping_filtered[key]['common_name']
    display_names.append(f'{key} ("{common_name}")' if common_name else key)
    display_name_mapper[display_names[-1]] = key

protein_display_name_mapper = {}
for key in list(uniprot_mapping_filtered.keys()):
    names = list(uniprot_mapping_filtered[key]['protein'].keys())
    
    for i in range(len(names)):
        names[i] += ' ({0})'.format(', '.join(uniprot_mapping_filtered[key]['protein'][names[i]]))
    
    protein_display_name_mapper[key] = names


app = Flask(__name__)
CORS(app, supports_credentials=True)

def query_filter(items, value) -> list:
    return list(filter(lambda e: (e or '').lower().find((value or '').lower()) > -1, items))[:10]

@app.route('/get_organisms', methods=['GET'])
def get_organisms() -> list:
    return display_names

@app.route('/query_organism_selections', methods=['POST'])
def query_organism_selections() -> list:
    query = request.get_json()['query']
    names = query_filter(display_names, query)
    return names

@app.route('/query_protein_selections', methods=['POST'])
def query_protein_selections() -> dict:
    data = request.get_json()
    organism = display_name_mapper[data['organism']]
    proteins = query_filter(protein_display_name_mapper[organism], data['query'])
    return proteins


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
