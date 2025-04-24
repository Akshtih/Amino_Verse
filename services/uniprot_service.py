import requests
import json
from flask import current_app

def get_protein_function(protein_name):
    """
    Query UniProt API to get protein function information
    """
    try:
        # UniProt API endpoint
        url = f"https://rest.uniprot.org/uniprotkb/search?query={protein_name}+AND+organism_id:9606&format=json"
        
        response = requests.get(url)
        response.raise_for_status()
        
        # Ensure we have valid JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            return {'error': f"Invalid JSON response from UniProt API"}
        
        # Process the response to extract relevant information
        if data.get('results') and len(data['results']) > 0:
            protein_data = data['results'][0]
            
            # Extract gene names safely
            gene_names = []
            if protein_data.get('genes') and len(protein_data['genes']) > 0:
                gene_name_list = protein_data['genes'][0].get('geneName', [])
                for gene in gene_name_list:
                    # Check if the gene is a dictionary with a 'value' key
                    if isinstance(gene, dict) and 'value' in gene:
                        gene_names.append(gene['value'])
                    # If it's a string, add it directly
                    elif isinstance(gene, str):
                        gene_names.append(gene)
            
            # Extract function information
            function_info = {
                'id': protein_data.get('primaryAccession', ''),
                'name': protein_data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', ''),
                'function': next((comment.get('texts', [{}])[0].get('value', '') 
                               for comment in protein_data.get('comments', []) 
                               if comment.get('commentType') == 'FUNCTION'), 
                              'Function information not available'),
                'gene_names': gene_names,
                'organism': protein_data.get('organism', {}).get('scientificName', '')
            }
            
            return function_info
        else:
            return {'error': 'No protein information found'}
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching data from UniProt: {str(e)}"}
    except Exception as e:
        # Catch any other unexpected errors
        return {'error': f"Unexpected error processing UniProt data: {str(e)}"}