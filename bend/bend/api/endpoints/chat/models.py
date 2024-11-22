from typing import List

from pydantic import BaseModel, Field


class TaxItem(BaseModel):
    """
    Represents credit or deduction in a tax return.
    """
    name: str = Field(..., description="Name of the credit or deduction applicable to user.")
    explanation: str = Field(..., description="Explanation of why user is applicable to credit or deduction.")
    amount: str = Field(..., description="Amount of credit or deduction that applies to user.")


class SelectItems(BaseModel):
    """
    Selects credits and deductions applicable to user. Select this tool only when you have gathered all possible information.
    """
    salary: float = Field(..., description="The salary of the user.")
    credits: List[TaxItem] = Field(..., description="List of credits applicable to user")
    deductions: List[TaxItem] = Field(..., description="List of deductions applicable to user")


class AskFollowup(BaseModel):
    """
    Asks user a follow question or response to gather more information. Use this tool to gather all the information you need
    to conclusively identify all credits and deductions that are application to user.
    """
    response: str = Field(..., description="The response to follow up in chat.")
