from utils.math_operations import MathOperations
from utils.error_type import ErrorType
from utils.handlers.non_linear_equations_handler import NonLinearEquationsHandler
from utils.errors.common_errors import (
    MaxIterationsReachedError,
    ToleranceNotMetError,
    FunctionZeroValueError,
    DerivativeZeroValueError
)
from utils.errors.non_linear_equations_errors import FalsePositionErrors
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
            if error_type == "relative":
                error = ErrorType.relative_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x) / abs(x)
            else:
                error = ErrorType.absolute_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))

        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()
        if f_value == 0:
            raise FunctionZeroValueError()

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result

    @staticmethod
    @NonLinearEquationsHandler.handle_response
    def newton_raphson_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        error_type: str
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
            if error_type == "relative":
                error = ErrorType.relative_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x) / abs(x)
            else:
                error = ErrorType.absolute_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))
            print(iteration_data)

        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()
        if f_value == 0:
            raise FunctionZeroValueError()
        if f_derivative_value == 0:
            raise DerivativeZeroValueError()

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result

    @staticmethod
    @NonLinearEquationsHandler.handle_response
    def multiple_roots_service(
        initial_guess: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        error_type: str
    ) -> Dict[str, Any]:
        iteration_data = []
        x = initial_guess
        f_value = MathOperations.evaluate_function(function_expression, x)
        derivate_expression = MathOperations.get_derivative(function_expression)
        f_derivative_value = MathOperations.evaluate_function(derivate_expression, x)
        second_derivative_expression = MathOperations.get_derivative(derivate_expression)
        second_f_derivative_value = MathOperations.evaluate_function(second_derivative_expression, x)
        error = 100
        iteration_count = 0
        iteration_data.append((iteration_count, x, f_value, error))

        while error > tolerance and f_value != 0 and f_derivative_value != 0 and iteration_count < max_iterations:
            x_new = x - (f_value * f_derivative_value) / ((f_derivative_value ** 2) - f_value * second_f_derivative_value)
            f_value = MathOperations.evaluate_function(function_expression, x_new)
            f_derivative_value = MathOperations.evaluate_function(derivate_expression, x_new)
            second_f_derivative_value = MathOperations.evaluate_function(second_derivative_expression, x_new)
            iteration_count += 1
            if error_type == "relative":
                error = ErrorType.relative_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x) / abs(x)
            else:
                error = ErrorType.absolute_error_non_linear_equation(x_new, x)
                #error = abs(x_new - x)
            x = x_new
            iteration_data.append((iteration_count, x, f_value, error))

        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()
        if f_value == 0:
            raise FunctionZeroValueError()
        if f_derivative_value == 0:
            raise DerivativeZeroValueError()

        result = {
            "root": x,
            "iterations": iteration_data
        }
        return result

    @staticmethod
    @NonLinearEquationsHandler.handle_response
    def false_position_service(
        left_bound: float,
        right_bound: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        error_type: str
    ) -> Dict[str, Any]:
        iteration_data = []
        function_left_bound = MathOperations.evaluate_function(function_expression, left_bound)
        function_right_bound = MathOperations.evaluate_function(function_expression, right_bound)
        iteration_count = 0
        error = 100

        if function_left_bound * function_right_bound > 0:
            raise FalsePositionErrors.RangeNotContainingRootError()

        root_approximation = left_bound
        iteration_data.append((iteration_count, left_bound, function_left_bound, error))

        while error > tolerance and iteration_count < max_iterations:
            if function_right_bound - function_left_bound == 0:
                break

            next_bound = right_bound - (function_right_bound * (right_bound - left_bound)) / (function_right_bound - function_left_bound)
            function_next_bound = MathOperations.evaluate_function(function_expression, next_bound)

            if error_type == "relative":
                error = ErrorType.relative_error_non_linear_equation(next_bound, root_approximation)
                #error = abs(x_new - x) / abs(x)
            else:
                error = ErrorType.absolute_error_non_linear_equation(next_bound, root_approximation)
                #error = abs(x_new - x)

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

        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()

        result = {
            "root": root_approximation,
            "iterations": iteration_data
        }
        return result

    @staticmethod
    @NonLinearEquationsHandler.handle_response
    def bisection_service(
        left_bound: float,
        right_bound: float,
        tolerance: float,
        max_iterations: int,
        function_expression: str,
        error_type: str
    ) -> Dict[str, Any]:
        iteration_data = []
        f_left = MathOperations.evaluate_function(function_expression, left_bound)
        f_right = MathOperations.evaluate_function(function_expression, right_bound)

        if f_left == 0:
            return {"root": left_bound, "iterations": [(0, left_bound, f_left, 0)]}
        elif f_right == 0:
            return {"root": right_bound, "iterations": [(0, right_bound, f_right, 0)]}

        iteration_count = 0
        mid_point = (left_bound + right_bound) / 2
        f_mid = MathOperations.evaluate_function(function_expression, mid_point)
        error = abs(0 - f_mid)
        prev_mid_point = mid_point
        iteration_data.append((iteration_count, mid_point, f_mid, error))

        while error > tolerance and f_mid != 0 and iteration_count < max_iterations:
            if f_left * f_mid < 0:
                right_bound = mid_point
                f_right = MathOperations.evaluate_function(function_expression, right_bound)
            else:
                left_bound = mid_point
                f_left = MathOperations.evaluate_function(function_expression, left_bound)

            prev_mid_point = mid_point
            mid_point = (left_bound + right_bound) / 2
            f_mid = MathOperations.evaluate_function(function_expression, mid_point)
            if error_type == "relative":
                error = ErrorType.relative_error_non_linear_equation(mid_point, prev_mid_point)
                #error = abs(x_new - x) / abs(x)
            else:
                error = ErrorType.absolute_error_non_linear_equation(mid_point, prev_mid_point)
                #error = abs(x_new - x)
                
            iteration_count += 1
            iteration_data.append((iteration_count, mid_point, f_mid, error))

        if iteration_count >= max_iterations:
            raise MaxIterationsReachedError()
        if error > tolerance:
            raise ToleranceNotMetError()
        if f_mid == 0:
            raise FunctionZeroValueError()

        result = {
            "root": mid_point,
            "iterations": iteration_data
        }
        return result
