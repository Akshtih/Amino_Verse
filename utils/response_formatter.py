def format_protein_response(protein_name, function_data, structure_data, drug_data, interaction_data):
    """
    Format the combined protein data response
    """
    # Check for errors in each data source
    function_error = function_data.get('error')
    structure_error = structure_data.get('error')
    drug_error = drug_data.get('error')
    interaction_error = interaction_data.get('error')
    
    response = {
        "protein": protein_name,
        "function": function_data if not function_error else {"status": "error", "message": function_error},
        "structure": structure_data if not structure_error else {"status": "error", "message": structure_error},
        "drug_associations": drug_data if not drug_error else {"status": "error", "message": drug_error},
        "interactions": interaction_data if not interaction_error else {"status": "error", "message": interaction_error},
    }
    
    # Add disease links if available (you might need to implement another service for this)
    # response["disease_links"] = disease_data
    
    return response