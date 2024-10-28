from pydantic import BaseModel
from typing import Literal, List


class SorInput(BaseModel):
    matrix_A: List[List[float]]
    solution_vector: List[float]
    initial_guess: List[float]
    omega: float
    tolerance: float
    max_iterations: int
    error_type: Literal['absolute', 'relative']
