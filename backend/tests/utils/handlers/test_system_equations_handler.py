from utils.errors.base_error import BaseError
from utils.handlers.system_equations_handler import SystemEquationsHandler


@SystemEquationsHandler.handle_response
def _ok() -> tuple:
    return {"root": [1.0], "iterations": []}, {"spectral_radius": 0.4}


@SystemEquationsHandler.handle_response
def _known_error() -> tuple:
    raise BaseError("known", "KNOWN")


@SystemEquationsHandler.handle_response
def _division() -> tuple:
    raise ZeroDivisionError()


@SystemEquationsHandler.handle_response
def _unknown() -> tuple:
    raise RuntimeError("boom")


@SystemEquationsHandler.handle_response
def _runtime_warning_div_zero() -> tuple:
    raise RuntimeWarning("divide by zero encountered in divide")


@SystemEquationsHandler.handle_response
def _runtime_warning_other() -> tuple:
    raise RuntimeWarning("other warning")


def test_system_handler_success_path() -> None:
    response = _ok()
    assert response["status"] == "success"
    assert response["spectral_radius"] == 0.4


def test_system_handler_known_error_path() -> None:
    response = _known_error()
    assert response["error"]["code"] == "KNOWN"


def test_system_handler_zero_division_path() -> None:
    response = _division()
    assert response["error"]["code"] == "DIVISION_BY_ZERO"


def test_system_handler_unknown_error_path() -> None:
    response = _unknown()
    assert response["error"]["code"] == "UNKNOWN_ERROR"


def test_system_handler_runtime_warning_division_path() -> None:
    response = _runtime_warning_div_zero()
    assert response["error"]["code"] == "DIVISION_BY_ZERO"


def test_system_handler_runtime_warning_other_path() -> None:
    response = _runtime_warning_other()
    assert response["error"]["code"] == "CALCULATION_ERROR"
