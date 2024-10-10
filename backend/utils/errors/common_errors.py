from utils.errors.base_error import BaseError


class DivisionByZeroError(BaseError):
    def __init__(self, message: str = "Division by zero detected."):
        super().__init__(message, "DIVISION_BY_ZERO")

class FunctionEvaluationError(BaseError):
    def __init__(self, message: str = "Function evaluation error."):
        super().__init__(message, "FUNCTION_EVALUATION_ERROR")

class DerivativeError(BaseError):
    def __init__(self, message: str = "Error calculating derivative."):
        super().__init__(message, "DERIVATIVE_ERROR")

class MaxIterationsReachedError(BaseError):
    def __init__(self, message: str = "Was reached the maximum number of iterations."):
        super().__init__(message, "MAX_ITERATIONS_REACHED")

class ToleranceNotMetError(BaseError):
    def __init__(self, message: str = "The specified tolerance was not reached."):
        super().__init__(message, "TOLERANCE_NOT_MET")

class FunctionZeroValueError(BaseError):
    def __init__(self, message: str = "The F function takes a zero value."):
        super().__init__(message, "FUNCTION_ZERO_VALUE")

class DerivativeZeroValueError(BaseError):
    def __init__(self, message: str = "The derivative of F takes a zero value."):
        super().__init__(message, "DERIVATIVE_ZERO_VALUE")