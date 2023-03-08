import flask
from flask import Flask, request
from flask_cors import CORS
# import chemcuratepi
from chemcurate import uniprot_mapping_filtered
# import yaml

# with open('test.yaml') as f:
#     uniprot_mapping_filtered = yaml.load(f, Loader=yaml.FullLoader)


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/get_organisms', methods=['GET'])
def get_organisms() -> list:
    print('ape')
    return list(uniprot_mapping_filtered.keys())

@app.route('/proteins_for_organisms', methods=['POST'])
def proteins_for_organisms() -> list:
    organisms = request.get_json()['organisms']
    # print(organisms)
    # return '', 204
    return list(uniprot_mapping_filtered[organisms[0]]['protein'].keys())

def query_filter(items, value) -> list:
    return list(filter(lambda e: (e or '').lower().find((value or '').lower()) > -1, items))

@app.route('/query_organism_selections', methods=['POST'])
def query_organism_selections() -> dict:
    query = request.get_json()['query']
    keys = query_filter(list(uniprot_mapping_filtered.keys()), query)
    
    out = {}
    for key in keys:
        out[key] = uniprot_mapping_filtered[key]
        
    return out

# @app.route('/a', methods=['GET'])
# def a() -> dict:
#     return {'a': 'b',
#             'b': 'c'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
