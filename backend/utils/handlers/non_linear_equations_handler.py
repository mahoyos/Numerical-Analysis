from typing import Callable
from functools import wraps
from utils.handlers.response import ResponseHandler
from utils.errors.common_errors import (
    BaseError,
    DivisionByZeroError,
    FunctionEvaluationError,
)

class NonLinearEquationsHandler:
    @staticmethod
    def handle_response(func : Callable) -> Callable : 
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
