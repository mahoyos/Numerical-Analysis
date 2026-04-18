from utils.math_operations import MathOperations


def test_evaluate_function_returns_expected_value() -> None:
    value = MathOperations.evaluate_function("x**2 - 2", 2)
    assert value == 2.0


def test_get_derivative_returns_sympy_expression() -> None:
    derivative = MathOperations.get_derivative("x**3")
    assert str(derivative) == "3*x**2"
