import numpy as np

from utils.error_type import ErrorType


def test_absolute_error_non_linear_equation() -> None:
    assert ErrorType.absolute_error_non_linear_equation(3.0, 2.0) == 1.0


def test_relative_error_non_linear_equation() -> None:
    assert ErrorType.relative_error_non_linear_equation(3.0, 2.0) == 0.5


def test_absolute_error_system_equations() -> None:
    actual = np.array([2.0, 3.0])
    old = np.array([1.0, 1.0])
    assert ErrorType.absolute_error_system_equations(actual, old) == 2.0


def test_relative_error_system_equations() -> None:
    actual = np.array([2.0, 3.0])
    old = np.array([1.0, 1.0])
    assert ErrorType.relative_error_system_equations(actual, old) == 2.0
