import requests
import argparse
from fuzzy_system import calculate_risk

def fetch_claims_data(table_name):
    """
    Fetch claims data from the API.
    """
    url = f'http://127.0.0.1:8000/claims/api/claims/{table_name}/'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser(description='Calculate risks from claims data.')
    parser.add_argument('table', type=str, help='The type of claims table (e.g., education, osp)')
    parser.add_argument('claims', nargs='+', help='List of claims to include in the risk assessment')

    args = parser.parse_args()

    try:
        claims_data = fetch_claims_data(args.table)
        
        # Process the claims data
        variables_array = [(claim['claim_designation'], claim['impact'], claim['gdpr_compliance']) for claim in claims_data if claim['claim_designation'] in args.claims]
        
        risk_array = []
        
        for variables in variables_array:
            calculated_risk, risk_level = calculate_risk(variables[1], variables[2])
            risk_array.append((variables[0], calculated_risk, risk_level))

        # Get the overall maximum risk value and its corresponding level
        max_risk_tuple = max(risk_array, key=lambda x: x[1])
        max_risk = max_risk_tuple[1]
        max_risk_level = max_risk_tuple[2]

        # Remove the risk_value (element[1]) from each tuple in risk_array
        risk_array = [(designation, risk_level) for designation, _, risk_level in risk_array]

        print("The highest risk value is:", max_risk, "which corresponds to", max_risk_level)
        print("Calculated Risks with Corresponding Letters:", risk_array)
        
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
