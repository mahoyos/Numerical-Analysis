from utils.error_type import ErrorType
from utils.handlers.system_equations_handler import SystemEquationsHandler
from utils.errors.common_errors import (
    MaxIterationsReachedError,
    ToleranceNotMetError,
    BaseError,
    ConvergenceError,
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

        convergence_status = SystemEquationsUtils.verify_solution(matrix_A, x, solution_vector, tolerance)["status"]
        if convergence_status == "not_converged":
            raise ConvergenceError()

        omega_value = omega

        spectral_radius = SystemEquationsUtils.spectral_radius(matrix_A, "sor", omega=omega_value)

        result = {
            "root": x.tolist(),
            "iterations": iteration_data,
        }
        return result, {"spectral_radius": spectral_radius}

    @staticmethod
    @SystemEquationsHandler.handle_response
    def gauss_seidel_service(
        matrix_A: List[List[float]],
        solution_vector: List[float],
        initial_guess: List[float],
        tolerance: float,
        max_iterations: int,
        error_type: str
    ) -> Dict[str, Any]:
        print("Initial guess: ", initial_guess)
        try:
            # Convertir las entradas a arrays de numpy
            matrix_A = np.array(matrix_A, dtype=float)
            solution_vector = np.array(solution_vector, dtype=float)
            x = np.array(initial_guess, dtype=float)

            n = len(matrix_A)
            iteration_data = []

            for iteration_counter in range(max_iterations):
                x_old = x.copy()

                for i in range(n):
                    sum1 = sum(matrix_A[i][j] * x[j] for j in range(i))
                    sum2 = sum(matrix_A[i][j] * x_old[j] for j in range(i + 1, n))
                    x[i] = (solution_vector[i] - sum1 - sum2) / matrix_A[i][i]

                if error_type == "relative":
                    error = ErrorType.relative_error_system_equations(x, x_old)
                else:
                    error = ErrorType.absolute_error_system_equations(x, x_old)

                iteration_data.append([iteration_counter, x.copy().tolist(), error])

                if error < tolerance:
                    break

            if iteration_counter >= max_iterations - 1:
                raise MaxIterationsReachedError()
            if error > tolerance:
                raise ToleranceNotMetError()

            convergence_status = SystemEquationsUtils.verify_solution(matrix_A, x, solution_vector, tolerance)["status"]
            if convergence_status == "not_converged":
                raise ConvergenceError()

            spectral_radius = SystemEquationsUtils.spectral_radius(matrix_A, "gauss_seidel")

            result = {
                "root": x.tolist(),
                "iterations": iteration_data,
            }

            return result, {"spectral_radius": spectral_radius}

        except Exception as e:
            raise BaseError(str(e), "CALCULATION_ERROR")

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

            convergence_status = SystemEquationsUtils.verify_solution(matrix_A, x, solution_vector, tolerance)["status"]
            if convergence_status == "not_converged":
                raise ConvergenceError()

            spectral_radius = SystemEquationsUtils.spectral_radius(matrix_A, "jacobi")

            result = {
                "root": x.tolist(),
                "iterations": iteration_data,
            }

            return result, {"spectral_radius": spectral_radius}

        except Exception as e:
            raise BaseError(str(e), "CALCULATION_ERROR")
