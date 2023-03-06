import flask
from flask import Flask, request
from flask_cors import CORS
import chemcurate


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/get_uniprot_mapping', methods=['GET'])
def get_uniprot_mapping() -> dict:
    return chemcurate.uniprot_mapping
    # return {'a': 'b'}

@app.route('/a', methods=['GET'])
def a() -> dict:
    return {'a': 'b',
            'b': 'c'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
