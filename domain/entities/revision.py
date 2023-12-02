from pydantic import BaseModel, Field


class Revision(BaseModel):
    speaker_A: str = Field(description="speaker A")
    speaker_B: str = Field(description="speaker B")
    authentic_expression: str = Field(description="authentic expression")

