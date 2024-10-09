from typing import Callable
from functools import wraps
from utils.response_handler import ResponseHandler
from utils.errors.common_errors import (
    BaseError,
    DivisionByZeroError,
    FunctionEvaluationError,
)

class ErrorHandler:
    @staticmethod
    def handle_numerical_errors(func : Callable) -> Callable : 
        @wraps(func)
        def wrapper(*args, **kwargs):
            try :
                result = func(*args, **kwargs)
                return ResponseHandler.success_response(result)
            except BaseError as e:
                return ResponseHandler.error_response(e)
            except ZeroDivisionError:
                return ResponseHandler.error_response(DivisionByZeroError())
            except ValueError as e:
                return ResponseHandler.error_response(FunctionEvaluationError(str(e)))
            except Exception as e:
                return ResponseHandler.error_response(BaseError(str(e), "UNKNOWN_ERROR"))
        return wrapper
