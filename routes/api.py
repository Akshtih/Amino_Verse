from flask import Blueprint, request, jsonify
from services.uniprot_service import get_protein_function
from services.pdb_service import get_protein_structure
from services.drugbank_service import get_drug_associations
from services.protein_interactions_service import get_protein_interactions
from utils.response_formatter import format_protein_response

api_bp = Blueprint('api', __name__)

@api_bp.route('/protein/<protein_name>', methods=['GET'])
def get_protein_info(protein_name):
    """
    Get comprehensive information about a protein or gene
    """
    try:
        # Add debug logging
        print(f"Processing request for protein: {protein_name}")
        
        # Get biological function from UniProt
        function_data = get_protein_function(protein_name)
        print(f"UniProt function data: {function_data}")
        
        # Get 3D structure from PDB/AlphaFold
        structure_data = get_protein_structure(protein_name)
        print(f"PDB structure data: {structure_data}")
        
        # Get drug associations
        drug_data = get_drug_associations(protein_name)
        print(f"Drug association data: {drug_data}")
        
        # Get protein interactions
        interaction_data = get_protein_interactions(protein_name)
        print(f"Interaction data: {interaction_data}")
        
        # Format the response
        response = format_protein_response(
            protein_name, 
            function_data, 
            structure_data, 
            drug_data, 
            interaction_data
        )
        
        return jsonify(response)
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing request: {str(e)}\n{error_details}")
        return jsonify({"error": str(e), "details": error_details}), 500

@api_bp.route('/protein/<protein_name>/followup', methods=['POST'])
def followup_question(protein_name):
    """
    Handle follow-up questions about a specific protein
    """
    try:
        data = request.json
        question = data.get('question', '')
        
        # Process follow-up question based on its content
        # This is a placeholder - you'll need to implement logic to interpret different types of follow-up questions
        
        if "disease" in question.lower():
            # Get disease-specific information
            return jsonify({"message": f"Disease information for {protein_name}"})
        
        elif "structure" in question.lower():
            # Get more detailed structure information
            return jsonify({"message": f"Detailed structure information for {protein_name}"})
        
        elif "variant" in question.lower():
            # Get variant information
            return jsonify({"message": f"Variant information for {protein_name}"})
        
        else:
            # General follow-up
            return jsonify({"message": f"Additional information for {protein_name} regarding: {question}"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500