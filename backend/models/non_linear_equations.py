from pydantic import BaseModel


class FixedPointInput(BaseModel):
    initial_guess: float
    tolerance: float
    max_iterations: int
    function_expression: str
    g_expression: str

class NewtonRaphsonInput(BaseModel):
    initial_guess: float
    tolerance: float
    max_iterations: int
    function_expression: str