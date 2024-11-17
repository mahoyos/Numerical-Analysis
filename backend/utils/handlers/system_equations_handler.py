from typing import Callable
from functools import wraps
from utils.handlers.response import ResponseHandler
from utils.errors.common_errors import (
    BaseError,
    DivisionByZeroError,
    FunctionEvaluationError,
)
from numpy.linalg import LinAlgError
import warnings


class SystemEquationsHandler:
    @staticmethod
    def handle_response(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Convertir RuntimeWarning en excepción
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("error")  # Convertir warnings en excepciones
                try:
                    result, additional_fields = func(*args, **kwargs)
                    return ResponseHandler.success_response(result, **additional_fields)
                except BaseError as e:
                    print(f"Error: {str(e)}")
                    return ResponseHandler.error_response(e)
                except ZeroDivisionError:
                    return ResponseHandler.error_response(DivisionByZeroError())
                except LinAlgError as e:
                    return ResponseHandler.error_response(BaseError(str(e), "MATRIX_ERROR"))
                except ValueError as e:
                    return ResponseHandler.error_response(FunctionEvaluationError(str(e)))
                except RuntimeWarning as e:
                    if "divide by zero" in str(e):
                        return ResponseHandler.error_response(DivisionByZeroError())
                    print(f"Error: {str(e)}")
                    return ResponseHandler.error_response(BaseError(str(e), "CALCULATION_ERROR"))
                except Exception as e:
                    print(f"Error completo: {str(e)}")  # Para depuración
                    print(f"Tipo de error: {type(e)}")  # Para ver el tipo exacto de error
                    return ResponseHandler.error_response(BaseError(str(e), "UNKNOWN_ERROR"))
        return wrapper
