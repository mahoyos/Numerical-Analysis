from utils.math_operations import MathOperations
from typing import Dict, Any

class FixedPointService:
    @staticmethod
    def fixed_point_service(
        initial_guess : float,
        tolerance : float,
        max_iterations : int,
        function_expression : str,
        g_expression : str
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
