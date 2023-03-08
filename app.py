import flask
from flask import Flask, request
from flask_cors import CORS
# import chemcuratepi
from chemcurate import uniprot_mapping_filtered


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/get_organisms', methods=['GET'])
def get_organisms() -> list:
    print('ape')
    return list(uniprot_mapping_filtered.keys())

@app.route('/get_proteins', methods=['POST'])
def proteins_for_organisms() -> list:
    organisms = request.get_json()['organisms']
    print(organisms)
    return '', 204

# @app.route('/a', methods=['GET'])
# def a() -> dict:
#     return {'a': 'b',
#             'b': 'c'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
