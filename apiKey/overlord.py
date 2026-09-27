from langchain_core.tools import tool
from langchain_protocol import AgentCommand
from langgraph.runtime import get_runtime
from langchain.agents import create_agent
import numpy as np
import json

@tool
def suggestion() -> str:
    """Suggests the best walking or driving methods for the user to improve mobility.

    Returns:
        str: The suggested methods of driving or physical mobility.
    """
    return "Suggested methods: driving or mobility aids"


def rating(rating: int) -> None:
    """Rates the user's mobility.
    Parameters
        rating (int): The rating given by the user.
    
    Rules
        Rating must be between 1 and 5.
    """
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")
    # Save the rating to a file or database
    with open("rating.json", "w") as f:
        json.dump({"rating": rating}, f)




def drive() -> bool:
    """Initiates a driving action. 

    Returns:
        bool: True if the driving action was successfully initiated, False otherwise.
    """
    AgentCommand("drive")
    return True