from utils.errors.base_error import BaseError
from utils.handlers.non_linear_equations_handler import NonLinearEquationsHandler


@NonLinearEquationsHandler.handle_response
def _ok() -> dict:
    return {"root": 1.0, "iterations": []}


@NonLinearEquationsHandler.handle_response
def _known_error() -> dict:
    raise BaseError("known", "KNOWN")


@NonLinearEquationsHandler.handle_response
def _division() -> dict:
    raise ZeroDivisionError()


@NonLinearEquationsHandler.handle_response
def _unknown() -> dict:
    raise RuntimeError("boom")


@NonLinearEquationsHandler.handle_response
def _value_error() -> dict:
    raise ValueError("bad expression")


def test_handler_success_path() -> None:
    response = _ok()
    assert response["status"] == "success"


def test_handler_known_error_path() -> None:
    response = _known_error()
    assert response["status"] == "error"
    assert response["error"]["code"] == "KNOWN"


def test_handler_zero_division_path() -> None:
    response = _division()
    assert response["error"]["code"] == "DIVISION_BY_ZERO"


def test_handler_unknown_error_path() -> None:
    response = _unknown()
    assert response["error"]["code"] == "UNKNOWN_ERROR"


def test_handler_value_error_path() -> None:
    response = _value_error()
    assert response["error"]["code"] == "FUNCTION_EVALUATION_ERROR"
