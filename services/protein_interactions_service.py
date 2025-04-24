import requests
from flask import current_app

def get_protein_interactions(protein_name):
    """
    Query for protein-protein interactions, using STRING database
    """
    try:
        # First resolve the protein name to a STRING ID
        species = "9606"  # Human
        url = f"https://string-db.org/api/json/resolve?identifier={protein_name}&species={species}"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data or len(data) == 0:
            return {'error': 'Protein not found in STRING database'}
        
        # Get the first match
        string_id = data[0].get('stringId')
        
        # Now query for interactions
        interactions_url = f"https://string-db.org/api/json/interactions?identifier={string_id}&species={species}&limit=20"
        
        interactions_response = requests.get(interactions_url)
        interactions_response.raise_for_status()
        
        interactions_data = interactions_response.json()
        
        # Process and clean up the interaction data
        interaction_list = []
        for interaction in interactions_data:
            partner = {
                'protein': interaction.get('preferredName_B', 'Unknown'),
                'score': interaction.get('score', 0),
                'string_id': interaction.get('stringId_B', ''),
                'description': f"Interacts with {interaction.get('preferredName_B', 'Unknown')} with confidence score {interaction.get('score', 0)}",
            }
            interaction_list.append(partner)
        
        return {
            'protein_name': data[0].get('preferredName', protein_name),
            'string_id': string_id,
            'network_url': f"https://string-db.org/network/{string_id}",
            'interactions': interaction_list
        }
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching protein interaction data: {str(e)}"}