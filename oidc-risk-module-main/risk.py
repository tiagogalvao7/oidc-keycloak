from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import requests
from flask_cors import CORS
from scikit_fuzzy.fuzzy_system import calculate_risk
import os

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Risk and Compliance API',
          description='A simple API for calculating risks and GDPR compliance')

ns_risk = api.namespace('risk', description='Risk operations')
ns_compliance = api.namespace('compliance', description='Compliance operations')
ns_transaction = api.namespace('transaction', description='Transaction operations')

# Define a model for individual risk claim without risk_value
risk_claim_model = api.model('RiskClaim', {
    'designation': fields.String(required=True, description='Claim Designation'),
    'risk_level': fields.String(required=True, description='Risk Level')
})

# Define model for risk with an array of risk claims
risk_model = api.model('Risk', {
    'highest_risk_value': fields.Float(required=True, description='The highest risk value'),
    'highest_risk_level': fields.String(required=True, description='The highest risk level'),
    'calculated_risks': fields.List(fields.Nested(risk_claim_model), description='List of calculated risks without risk values')
})

# Define model for compliance
compliance_model = api.model('Compliance', {
    'compliance_percentage': fields.Float(required=True, description='Compliance Percentage')
})

# Define model for transaction with hash
transaction_model = api.model('Transaction', {
    'name': fields.String(required=True, description='Transaction Name'),
    'transaction': fields.String(required=True, description='Transaction Hash')
})

def fetch_claims_data(table_name):
    """
    Fetch claims data from the API.
    """
    try:
        serverEVM = os.environ.get('URL-EVM-API')
    except KeyError:
        print("Server not defined using localhost, it might not work!!!")
        serverEVM = "http://127.0.0.1:8000"
    
    app.logger.info('Using URL-EVM-API' + serverEVM)
    url = f'{serverEVM}/claims/api/claims/{table_name}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} {response.text}")

@ns_risk.route('/<string:table>')
@ns_risk.param('table', 'The type of claims table (e.g., education, osp)')
@ns_risk.param('claims', 'Comma-separated list of claims to include in the risk assessment', type=str, default='', _in='query')
class RiskResource(Resource):
    @ns_risk.marshal_with(risk_model)
    def get(self, table):
        claims_param = request.args.get('claims', '')  # Get the 'claims' parameter as a comma-separated string
        claims = claims_param.split(',') if claims_param else []  # Split by comma to get a list of claims
        try:
            claims_data = fetch_claims_data(table)
            variables_array = [(claim['claim_designation'], claim['impact'], claim['gdpr_compliance']) for claim in claims_data if claim['claim_designation'] in claims]
            
            risk_array = []
            for variables in variables_array:
                calculated_risk, risk_level = calculate_risk(variables[1], variables[2])
                risk_array.append((
                    variables[0],  # claim_designation
                    calculated_risk,  # risk_value
                    risk_level
                ))

            # Find the tuple with the maximum calculated_risk
            max_risk_tuple = max(risk_array, key=lambda x: x[1])
            max_risk = max_risk_tuple[1]*10
            max_risk_level = max_risk_tuple[2]

            # Prepare the calculated risks list for the response without risk_value
            calculated_risks = [
                {
                    'designation': designation,
                    'risk_level': risk_level
                }
                for designation, risk_value, risk_level in risk_array
            ]

            return {
                'highest_risk_value': round(max_risk,1),
                'highest_risk_level': max_risk_level,
                'calculated_risks': calculated_risks
            }
        except Exception as e:
            return {'error': str(e)}, 500

@ns_compliance.route('/<string:table>')
@ns_compliance.param('table', 'The type of claims table (e.g., education, osp)')
@ns_compliance.param('claims', 'Comma-separated list of claims to include in the compliance assessment', type=str, default='', _in='query')
class ComplianceResource(Resource):
    @ns_compliance.marshal_with(compliance_model)
    def get(self, table):
        claims_param = request.args.get('claims', '')  # Get the 'claims' parameter as a comma-separated string
        claims = claims_param.split(',') if claims_param else []  # Split by comma to get a list of claims
        try:
            claims_data = fetch_claims_data(table)
            compliance_percentage = calculate_compliance_percentage(claims_data, claims)
            return {'compliance_percentage': compliance_percentage}
        except Exception as e:
            return {'error': str(e)}, 500


def calculate_compliance_percentage(claims_data, requested_claims):
    """
    Calculate the percentage of claims compliant with GDPR.
    """
    total_claims = 0
    compliant_claims = 0
    
    for claim in claims_data:
        if claim['claim_designation'] in requested_claims:
            total_claims += 1
            if claim['gdpr_compliance'] == 1.0:
                compliant_claims += 1

    if total_claims == 0:
        return 0.0  # Avoid division by zero
    
    compliance_percentage = (compliant_claims / total_claims) * 100

    return round(compliance_percentage)

def fetch_transaction(name):
    """
    Fetch a specific transaction from the Django API.
    """
    """
    Fetch claims data from the API.
    """
    try:
        serverEVM = os.environ.get('URL-EVM-API')
    except KeyError:
        print("Server not defined using localhost, it might not work!!!")
        serverEVM = "http://127.0.0.1:8000"
    
    app.logger.info('Using URL-EVM-API' + serverEVM)
    url = f'{serverEVM}/claims/api/transactions/{name}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None  # Transaction not found, return None to handle in Flask
    else:
        # Handle any other error (e.g., 500)
        raise Exception(f"Error fetching transaction: {response.status_code} {response.text}")

def add_transaction(data):
    """
    Add a new transaction via the Django API.
    """
    try:
        serverEVM = os.environ.get('URL-EVM-API')
    except KeyError:
        print("Server not defined using localhost, it might not work!!!")
        serverEVM = "http://127.0.0.1:8000"
    
    app.logger.info('Using URL-EVM-API' + serverEVM)
    url = f'{serverEVM}/claims/api/transactions/add/'
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Error adding transaction: {response.status_code} {response.text}")

def update_transaction(data):
    """
    Update an existing transaction via the Django API.
    """
    try:
        serverEVM = os.environ.get('URL-EVM-API')
    except KeyError:
        print("Server not defined using localhost, it might not work!!!")
        serverEVM = "http://127.0.0.1:8000"
    
    app.logger.info('Using URL-EVM-API' + serverEVM)
    url = f"{serverEVM}/claims/api/transactions/update/{data['id']}/"
    response = requests.put(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error updating transaction: {response.status_code} {response.text}")


@ns_transaction.route('/<string:name>')
@ns_transaction.param('name', 'The name of the transaction')
class TransactionResource(Resource):
    @ns_transaction.marshal_with(transaction_model)
    def get(self, name):
        try:
            transaction = fetch_transaction(name)
            return transaction
        except Exception as e:
            return {'error': str(e)}, 500

@ns_transaction.route('/add')
class AddTransactionResource(Resource):
    @ns_transaction.expect(transaction_model)
    def post(self):
        data = request.json
        try:
            # Try to fetch the transaction by name
            transaction = fetch_transaction(data['name'])
            
            if transaction:  # If the transaction exists, update it
                data['id'] = transaction['id']  # Assume Django API returns the transaction's ID
                response = update_transaction(data)  # Call to update function
                return response, 200  # Return status 200 for update
            else:
                # If no transaction exists, add it as a new one
                response = add_transaction(data)
                return response, 201  # Return status 201 for creation

        except requests.exceptions.RequestException as req_err:
            # Handle connection errors, timeouts, etc.
            return {'error': f'Error communicating with transaction API: {str(req_err)}'}, 500

        except Exception as e:
            # Handle any other general exceptions
            return {'error': f'Unexpected error: {str(e)}'}, 500


if __name__ == '__main__':
    app.run(debug=False, port=5001, host="0.0.0.0")
