import requests
from flask import current_app

def get_drug_associations(protein_name):
    """
    Query DrugBank or ChEMBL API to get drug association information
    
    Note: DrugBank requires authentication and has limited API access.
    ChEMBL is more open but may require different query patterns.
    This is a simplified example.
    """
    try:
        # Using ChEMBL API for drug target information
        # First get the ChEMBL target ID for the protein
        target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search?q={protein_name}&limit=1&format=json"
        target_response = requests.get(target_url)
        target_response.raise_for_status()
        target_data = target_response.json()
        
        if not target_data.get('targets') or len(target_data['targets']) == 0:
            return {'error': 'No target information found in ChEMBL'}
        
        target_chembl_id = target_data['targets'][0].get('target_chembl_id')
        
        # Get drugs/compounds that interact with this target
        drugs_url = f"https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id={target_chembl_id}&limit=10&format=json"
        drugs_response = requests.get(drugs_url)
        drugs_response.raise_for_status()
        drugs_data = drugs_response.json()
        
        drug_list = []
        for activity in drugs_data.get('activities', []):
            drug = {
                'molecule_chembl_id': activity.get('molecule_chembl_id', ''),
                'molecule_name': activity.get('molecule_name', 'Unknown compound'),
                'activity_type': activity.get('standard_type', ''),
                'activity_value': f"{activity.get('standard_value', 'N/A')} {activity.get('standard_units', '')}",
            }
            drug_list.append(drug)
        
        return {
            'target_chembl_id': target_chembl_id,
            'target_name': target_data['targets'][0].get('pref_name', ''),
            'drugs': drug_list
        }
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching drug association data: {str(e)}"}