from langchain_core.tools import tool
from pydantic import BaseModel, Field

class IntegralList(BaseModel):
    expressions: list[str] = Field(description="A list of mathematical expressions for the integrals.")

# global storage
submitted_integrals: set[str] = set()

@tool
def get_previously_submitted_integrals() -> list[str]:
    """Retrieve the list of all submitted integrals.
    Use this tool to check existing submissions and ensure your newly generated 
    integrals are diverse and do not duplicate these."""
    global submitted_integrals
    print(f"Retrieving previously submitted integrals: {submitted_integrals}")
    return list(submitted_integrals)

@tool(args_schema=IntegralList)
def submit_generated_integrals(expressions: list[str]) -> str:
    """
    Submits the final list of generated integrals to the system.
    ALWAYS use this tool to submit your final list of selected integrals.
    """
    global submitted_integrals
    
    old_count = len(submitted_integrals)
    submitted_integrals.update(expressions)
    added_count = len(submitted_integrals) - old_count
    
    print(f"Submitting the following expressions:\n{expressions}")
    print(f"Added {added_count} unique expressions.\n")
    
    return f"SUCCESS: {added_count} unique expressions have been saved successfully. You must now end the conversation."


