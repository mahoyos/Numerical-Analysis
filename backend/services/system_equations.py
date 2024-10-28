from utils.math_operations import MathOperations
from utils.errors.non_linear_equations_errors import FalsePositionErrors
from typing import Dict, Any, List
import numpy as np


class SystemEquationsService:
    @staticmethod
    def sor_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        initial_guess: List[float],
        tolerance: float,
        max_iterations: int,
        omega: float,
        error_type: str
    ) -> Dict[str, Any]:
        iteration_data = []
        matrix_D = np.diag(np.diag(matrix_A))
        matrix_L = -1 * np.tril(matrix_A, -1)
        matrix_U = -1 * np.triu(matrix_A, 1)
        iteration_counter = 0
        error = 100
        x = np.array(initial_guess)

        while error > tolerance and iteration_counter < max_iterations:
            matrix_T = np.linalg.inv(matrix_D - omega * matrix_L) @ ((1 - omega) * matrix_D + omega * matrix_U)
            matrix_C = omega * np.linalg.inv(matrix_D - omega * matrix_L) @ np.array(solution_vector)
            x_new = matrix_T @ x + matrix_C
            error = np.linalg.norm(x_new - x, ord=np.inf)
            x = x_new
            iteration_counter += 1
            iteration_data.append([iteration_counter, x_new.tolist(), error])  # Convertimos x_new a lista

        result = {
            "root": x.tolist(),  # Convertimos x a lista para que sea JSON serializable
            "iteration_data": iteration_data
        }

        return result