from flask import Flask, request, jsonify
from chempy import balance_stoichiometry
from chempy.util import periodic
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/balance', methods=['POST'])
def balance():
    data = request.get_json()
    reactants = data.get('reactants', [])
    products = data.get('products', [])
    try:
        reac, prod = balance_stoichiometry(set(reactants), set(products))
        result = {
            'reactants': {k: int(v) for k, v in reac.items()},
            'products': {k: int(v) for k, v in prod.items()}
        }
        return jsonify({'success': True, 'balanced': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/')
def home():
    return 'ChemPy Balancer API is running.'

if __name__ == '__main__':
    app.run(debug=True)
