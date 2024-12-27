from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    """
    Schema for validation error response.

    Attributes:
        error (str): A description of the validation error.
                     Example: "field_name: validation message".
    """

    error: str = Field(..., example="field_name: validation message")
