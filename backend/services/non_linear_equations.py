from utils.math_operations import MathOperations
from utils.handlers.non_linear_equations_handler import NonLinearEquationsHandler
from utils.errors.common_errors import MaxIterationsReachedError, ToleranceNotMetError
from typing import Dict, Any


class NonLinearEquationsService:
    @staticmethod
    @NonLinearEquationsHandler.handle_response
    def fixed_point_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        g_expression: str,
        error_type: str
    ) -> Dict[str, Any]:
        print(error_type)
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
            if error_type == 'relative' and x != 0 :
                error = abs(x_new - x) / abs(x)
            else :
                error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))
        
        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result
