from utils.errors.base_error import BaseError
from utils.errors.common_errors import (
    DivisionByZeroError,
    FunctionEvaluationError,
    DerivativeError,
    MaxIterationsReachedError,
    ToleranceNotMetError,
    FunctionZeroValueError,
    DerivativeZeroValueError,
    ConvergenceError,
    SpectralRadiusError,
)
from utils.errors.non_linear_equations_errors import FalsePositionErrors


def test_base_error_properties() -> None:
    err = BaseError("message", "CODE")
    assert err.message == "message"
    assert err.error_code == "CODE"


def test_common_error_types_have_codes() -> None:
    assert DivisionByZeroError().error_code == "DIVISION_BY_ZERO"
    assert FunctionEvaluationError().error_code == "FUNCTION_EVALUATION_ERROR"
    assert DerivativeError().error_code == "DERIVATIVE_ERROR"
    assert MaxIterationsReachedError().error_code == "MAX_ITERATIONS_REACHED"
    assert ToleranceNotMetError().error_code == "TOLERANCE_NOT_MET"
    assert FunctionZeroValueError().error_code == "FUNCTION_ZERO_VALUE"
    assert DerivativeZeroValueError().error_code == "DERIVATIVE_ZERO_VALUE"
    assert ConvergenceError().error_code == "CONVERGENCE_ERROR"


def test_spectral_radius_error_message_contains_value() -> None:
    err = SpectralRadiusError(1.25)
    assert "1.25" in err.message


def test_false_position_nested_error() -> None:
    err = FalsePositionErrors.RangeNotContainingRootError()
    assert err.error_code == "RANGE_NOT_CONTAINING_ROOT"


def test_false_position_base_error_constructor() -> None:
    err = FalsePositionErrors("custom", "CUSTOM")
    assert err.error_code == "CUSTOM"
