from pydantic import BaseModel
from typing import Literal

class FixedPointInput(BaseModel):
    initial_guess: float
    tolerance: float
    max_iterations: int
    function_expression: str
    g_expression: str
    error_type : Literal['absolute', 'relative']
