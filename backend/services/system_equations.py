from utils.error_type import ErrorType
from utils.handlers.system_equations_handler import SystemEquationsHandler
from utils.errors.common_errors import (
    MaxIterationsReachedError,
    ToleranceNotMetError,
    BaseError
)
from utils.system_equations import SystemEquationsUtils
from typing import Dict, Any, List
import numpy as np


class SystemEquationsService:
    @staticmethod
    @SystemEquationsHandler.handle_response
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
        spectral_radius_value = SystemEquationsUtils.spectral_radius(matrix_A)
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
            if error_type == "relative":
                error = ErrorType.relative_error_system_equations(x_new, x)
            else:
                error = ErrorType.absolute_error_system_equations(x_new, x)

            x = x_new
            iteration_counter += 1
            iteration_data.append([iteration_counter, x_new.tolist(), error])

        if iteration_counter >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()

        result = {
            "root": x.tolist(),
            "iteration_data": iteration_data,
            "spectral_radius": spectral_radius_value
        }

        return result

    @staticmethod
    @SystemEquationsHandler.handle_response
    def gauss_seidel_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        tolerance: float,
        initial_guess: List[float],
        max_iterations: int,
        error_type: str
    ) -> Dict[str, Any]:
        x = np.array(initial_guess, dtype=float)
        iteration_data = []
        spectral_radius_value = SystemEquationsUtils.spectral_radius(matrix_A)
        n = len(matrix_A)
        error = tolerance + 1
        iteration_counter = 0

        while error > tolerance and iteration_counter < max_iterations:
            x_new = np.copy(x)
            for i in range(n):
                sum_val = sum(matrix_A[i][j] * x_new[j] for j in range(n) if j != i)
                x_new[i] = (solution_vector[i] - sum_val) / matrix_A[i][i]

            if error_type == "relative":
                error = ErrorType.relative_error_system_equations(x_new, x)
            else:
                error = ErrorType.absolute_error_system_equations(x_new, x)

            x = x_new
            iteration_counter += 1
            iteration_data.append([iteration_counter, x.tolist(), error])

        if iteration_counter >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()

        result = {
            "root": x.tolist(),
            "iteration_data": iteration_data,
            "spectral_radius": spectral_radius_value
        }
        return result

    @staticmethod
    @SystemEquationsHandler.handle_response
    def jacobi_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        initial_guess: List[float],
        tolerance: float,
        max_iterations: int,
        error_type: str
    ) -> Dict[str, Any]:
        try:
            x = np.array(initial_guess)
            iteration_data = []
            spectral_radius_value = SystemEquationsUtils.spectral_radius(matrix_A)
            matrix_D = np.diag(np.diag(matrix_A))
            matrix_LU = matrix_A - matrix_D
            iteration_counter = 0
            error = tolerance + 1

            while error > tolerance and iteration_counter < max_iterations:
                x_new = np.linalg.inv(matrix_D) @ (np.array(solution_vector) - matrix_LU @ x)
                if error_type == "relative":
                    error = ErrorType.relative_error_system_equations(x_new, x)
                else:
                    error = ErrorType.absolute_error_system_equations(x_new, x)

                x = x_new
                iteration_counter += 1
                iteration_data.append([iteration_counter, x.tolist(), error])

            if iteration_counter >= max_iterations:
                raise MaxIterationsReachedError()
            if error > tolerance:
                raise ToleranceNotMetError()

            return {
                "root": x.tolist(),
                "iterations": iteration_data,
                "spectral_radius": spectral_radius_value
            }

        except Exception as e:
            raise BaseError(str(e), "CALCULATION_ERROR")