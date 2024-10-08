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
    def newton_raphson_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str
    ) -> Dict[str, Any]:
        iteration_data = []
        x = initial_guess
        derivative_expression = MathOperations.get_derivative(function_expression)
        f_value = MathOperations.evaluate_function(function_expression, x)
        f_derivative_value = MathOperations.evaluate_function(derivative_expression, x)
        error = 100
        iteration_count = 0
        iteration_data.append((iteration_count, x, f_value, error))

        while error > tolerance and f_value != 0 and f_derivative_value != 0 and iteration_count < max_iterations:
            x_new = x - f_value / f_derivative_value
            f_value = MathOperations.evaluate_function(function_expression, x_new)
            f_derivative_value = MathOperations.evaluate_function(derivative_expression, x_new)
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

    @staticmethod
    def false_position_service(
        left_bound: float,
        right_bound: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str
    ) -> Dict[str, Any]:
        iteration_data = []
        function_left_bound = MathOperations.evaluate_function(function_expression, left_bound)
        function_right_bound = MathOperations.evaluate_function(function_expression, right_bound)
        iteration_count = 0
        error = 100

        if function_left_bound * function_right_bound > 0:
            return {
                "root": left_bound,
                "iterations": iteration_data,
                "message": "The method cannot be applied: The function has the same sign at both ends.",
                "message_type": 0
            }

        root_approximation = left_bound
        iteration_data.append((iteration_count, left_bound, function_left_bound, error))

        while error > tolerance and iteration_count < max_iterations:
            if function_right_bound - function_left_bound == 0:
                break

            next_bound = right_bound - (function_right_bound * (right_bound - left_bound)) / (function_right_bound - function_left_bound)
            function_next_bound = MathOperations.evaluate_function(function_expression, next_bound)

            error = abs(next_bound - root_approximation)

            if error <= tolerance:
                break

            iteration_count += 1
            root_approximation = next_bound
            iteration_data.append((iteration_count, next_bound, function_next_bound, error))

            if function_next_bound == 0:
                break
            elif function_left_bound * function_next_bound < 0:
                right_bound = next_bound
                function_right_bound = function_next_bound
            else:
                left_bound = next_bound
                function_left_bound = function_next_bound

        if error > tolerance:
            return {
                "root": root_approximation,
                "iterations": iteration_data,
                "message": f"Maximum iterations ({max_iterations}) reached or tolerance not met, returning best approximation.",
                "message_type": 0
            }
        else:
            return {
                "root": root_approximation,
                "iterations": iteration_data,
                "message": f"Solution found with the specified tolerance in {root_approximation}.",
                "message_type": 1
            }
