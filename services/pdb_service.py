import requests
import json
from flask import current_app

def get_protein_structure(protein_name):
    """
    Query PDB/AlphaFold API to get protein structure information
    """
    try:
        # First check PDB for experimental structures
        pdb_url = f"https://search.rcsb.org/rcsbsearch/v2/query?json={{'query': {{'type': 'terminal', 'service': 'text', 'parameters': {{'attribute': 'rcsb_entity_source_organism.taxonomy_lineage.name', 'operator': 'exact_match', 'value': 'Homo sapiens'}}}}, 'return_type': 'entry', 'request_options': {{'results_content_type': ['experimental']}}, 'query_node_id': 0}}"
        
        pdb_response = requests.get(pdb_url)
        pdb_response.raise_for_status()
        
        try:
            pdb_data = pdb_response.json()
        except json.JSONDecodeError:
            pdb_data = {'error': 'Invalid JSON response from PDB API'}
        
        # If PDB data is available, use it
        if pdb_data.get('result_set') and len(pdb_data['result_set']) > 0:
            structure_ids = [result.get('identifier') for result in pdb_data['result_set']]
            
            # Get details for the first structure
            if structure_ids:
                structure_url = f"https://data.rcsb.org/rest/v1/core/entry/{structure_ids[0]}"
                structure_response = requests.get(structure_url)
                structure_response.raise_for_status()
                
                try:
                    structure_details = structure_response.json()
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON response from PDB structure API'}
                
                return {
                    'source': 'PDB (Experimental)',
                    'pdb_id': structure_ids[0],
                    'title': structure_details.get('struct', {}).get('title', ''),
                    'resolution': structure_details.get('pdbx_vrpt_summary', {}).get('pdbresolution', 'N/A'),
                    'method': structure_details.get('exptl', [{}])[0].get('method', '') if structure_details.get('exptl') else '',
                    'structure_view_url': f"https://www.rcsb.org/3d-view/{structure_ids[0]}",
                    'all_structures': structure_ids[:5]  # Return up to 5 structures
                }
        
        # If no PDB data or as an alternative, check AlphaFold
        alphafold_url = f"https://alphafold.ebi.ac.uk/api/prediction/{protein_name}"
        alphafold_response = requests.get(alphafold_url)
        
        if alphafold_response.status_code == 200:
            try:
                alphafold_data = alphafold_response.json()
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON response from AlphaFold API'}
            
            return {
                'source': 'AlphaFold (Predicted)',
                'alphafold_id': alphafold_data.get('entryId', ''),
                'confidence': alphafold_data.get('meanConfidence', ''),
                'structure_view_url': f"https://alphafold.ebi.ac.uk/entry/{alphafold_data.get('entryId', '')}",
                'model_date': alphafold_data.get('modelCreatedDate', '')
            }
        
        # If neither found
        return {'error': 'No structure information found in PDB or AlphaFold'}
    
    except requests.exceptions.RequestException as e:
        return {'error': f"Error fetching structure data: {str(e)}"}