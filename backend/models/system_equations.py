from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class SystemsEquationsInput(BaseModel):
    matrix_A: List[List[float]]
    solution_vector: List[float]
    initial_guess: Optional[List[float]] = Field(default=None)
    omega: Optional[float] = Field(default=None)
    tolerance: float
    max_iterations: int
    error_type: Literal['absolute', 'relative']
    method: Literal['sor', 'gauss-seidel', 'jacobi']
