from utils.math_operations import MathOperations
from typing import Dict, Any


class NonLinearEquationsService:
    @staticmethod
    def fixed_point_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        g_expression: str
    ) -> Dict[str, Any]:
        iteration_data = []
        x = initial_guess
        f_value = MathOperations.evaluate_function(function_expression, x)
        error = 100
        iteration_count = 0
        iteration_data.append((iteration_count, x, f_value, error))

        while error > tolerance and f_value != 0 and iteration_count < max_iterations:
            x_new = MathOperations.evaluate_function(g_expression, x)
            f_value = MathOperations.evaluate_function(function_expression, x_new)
            iteration_count += 1
            error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result

    @staticmethod
    def multiple_roots_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str
    ) -> Dict[str, Any]:
        iteration_data = []
        x = initial_guess
        f_value = MathOperations.evaluate_function(function_expression, x)
        derivate_expression = MathOperations.get_derivative(function_expression)
        derivate_value = MathOperations.evaluate_function(derivate_expression, x)
        second_derivative_expression = MathOperations.get_derivative(derivate_expression)
        second_derivate_value = MathOperations.evaluate_function(second_derivative_expression, x)
        error = 100
        iteration_count = 0
        iteration_data.append((iteration_count, x, f_value, error))

        while error > tolerance and f_value != 0 and derivate_value != 0 and iteration_count < max_iterations:
            x_new = x - (f_value * derivate_value) / ((derivate_value ** 2) - f_value * second_derivate_value)
            f_value = MathOperations.evaluate_function(function_expression, x_new)
            derivate_value = MathOperations.evaluate_function(derivate_expression, x_new)
            second_derivate_value = MathOperations.evaluate_function(second_derivative_expression, x_new)
            iteration_count += 1
            error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result