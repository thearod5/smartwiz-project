# Pydantic Model for Tax Credit/Deduction
from typing import Literal

from pydantic import BaseModel, Field


class Record(BaseModel):
    """
    Represents a credit or deduction in a tax return.
    """
    type: Literal["credit", "deduction"] = Field(..., description="Specified whether record is credit or deduction.")
    name: str = Field(..., description="The name of the credit or deduction.")
    source: str = Field(..., description="Link to source containing details about credit or deduction.")


class RecordSummary(BaseModel):
    """
    Summarizes a credit or deduction webpage, if it is describing one in detail.
    """
    summary: str = Field(..., description=(
        "Summary about applicability, conditions, or important information to know about credit or deduction. "
        "Write summary as a paragraph of prose and make it concise. "
        "If content does not have credit or deduction provided, leave as `NA`"
    ))


# Pydantic Model for URL Data
class URLBatch(BaseModel):
    url: str
    explored: bool = False
