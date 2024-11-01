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
            iteration_data.append([iteration_counter, x_new.tolist(), error])

        result = {
            "root": x.tolist(),
            "iteration_data": iteration_data
        }

        return result

    @staticmethod
    def gauss_seidel_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        tolerance: float,
        max_iterations: int,
        error_type: str
    ) -> Dict[str, Any]:
        n = len(matrix_A)
        x = np.zeros(len(matrix_A))
        iteration_data = []

        for iteration_counter in range(max_iterations):
            x_old = x.copy()

            for i in range(n):
                sum1 = sum(matrix_A[i][j] * x[j] for j in range(i))
                sum2 = sum(matrix_A[i][j] * x_old[j] for j in range(i + 1, n))
                x[i] = (solution_vector[i] - sum1 - sum2) / matrix_A[i][i]

            error = np.linalg.norm(x - x_old, np.inf) / np.linalg.norm(x, np.inf)
            iteration_data.append([iteration_counter, x.copy().tolist(), error])

            if error < tolerance:
                break

        result = {
            "root": x.tolist(),
            "iteration_data": iteration_data,
        }

        return result

    @staticmethod
    def jacobi_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        initial_guess: List[float],
        tolerance: float,
        max_iterations: int,
        error_type: str
    ) -> Dict[str, Any]:
        x = np.array(initial_guess)
        iteration_data = []

        matrix_D = np.diag(np.diag(matrix_A))
        matrix_LU = matrix_A - matrix_D
        iteration_counter = 0
        error = tolerance + 1
        while error > tolerance and iteration_counter < max_iterations:
            x_new = np.linalg.inv(matrix_D) @ (np.array(solution_vector) - matrix_LU @ x)
            error = np.linalg.norm(x_new - x, ord=np.inf) / np.linalg.norm(x_new, ord=np.inf)
            x = x_new
            iteration_counter += 1
            iteration_data.append([iteration_counter, x.tolist(), error])

        result = {
            "root": x.tolist(),
            "iteration_data": iteration_data,
        }

        return result
