from crew import LegalMateAi

def summarize(contract_text: str) -> str:
    """
    Summarizes the contract text using the LegalMateAi crew.
    
    Args:
        contract_text (str): The text of the contract to be summarized.
    
    Returns:
        str: The summary of the contract.
    """
    inputs = {
        'contract_text': contract_text
    }
    
    try:
        print(inputs)
        response = LegalMateAi().crew().kickoff(inputs=inputs)
        # Extract final output string from CrewOutput
        if hasattr(response, "raw"):
            return response.raw
        elif hasattr(response, "output"):
            return response.output
        elif hasattr(response, "final_output"):
            return response.final_output
        else:
            return str(response)
    except Exception as e:
        raise Exception(f"An error occurred while summarizing the contract: {e}")