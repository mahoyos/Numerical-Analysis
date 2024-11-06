import numpy as np


class ErrorType:
    @staticmethod
    def absolute_error(
        actual_value: float,
        old_value: float
    ) -> float:
        return abs(actual_value - old_value)
    
    @staticmethod
    def relative_error_non_linear_equation(
        actual_value: float,
        old_value: float
    ) -> float:
        return abs(actual_value - old_value) / abs(old_value)