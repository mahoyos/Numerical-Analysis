import numpy as np


class ErrorType:
    @staticmethod
    def absolute_error_non_linear_equation(
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
    
    @staticmethod
    def absolute_error_system_equations(
        actual_value: float,
        old_value: float
    ) -> float:
        return np.linalg.norm(actual_value - old_value, ord=np.inf)
    
    @staticmethod
    def relative_error_system_equations(
        actual_value: float,
        old_value: float
    ) -> float:
        return np.linalg.norm((actual_value - old_value) / old_value, ord=np.inf)