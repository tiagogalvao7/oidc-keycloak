import requests
import argparse

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

    return (compliant_claims / total_claims) * 100

def main():
    parser = argparse.ArgumentParser(description='Calculate GDPR compliance percentage from claims data.')
    parser.add_argument('table', type=str, help='The type of claims table (e.g., education, osp)')
    parser.add_argument('claims', nargs='+', help='List of claims to include in the compliance assessment')

    args = parser.parse_args()

    try:
        claims_data = fetch_claims_data(args.table)
        compliance_percentage = calculate_compliance_percentage(claims_data, args.claims)

        print(f"Percentage of compliant claims: {compliance_percentage:.2f}%")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
