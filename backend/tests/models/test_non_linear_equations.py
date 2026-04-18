import pytest
from pydantic import ValidationError

from models.non_linear_equations import FixedPointInput, BisectionInput


def test_fixed_point_input_valid_data() -> None:
    model = FixedPointInput(
        initial_guess=1.0,
        tolerance=1e-5,
        max_iterations=100,
        function_expression="x**2 - 2",
        g_expression="(x + 2/x)/2",
        error_type="absolute",
    )
    assert model.max_iterations == 100


def test_fixed_point_input_invalid_error_type() -> None:
    with pytest.raises(ValidationError):
        FixedPointInput(
            initial_guess=1.0,
            tolerance=1e-5,
            max_iterations=100,
            function_expression="x**2 - 2",
            g_expression="(x + 2/x)/2",
            error_type="invalid",
        )


def test_bisection_input_parses_numbers() -> None:
    model = BisectionInput(
        left_bound=0,
        right_bound=2,
        tolerance=0.001,
        max_iterations=25,
        function_expression="x - 1",
        error_type="relative",
    )
    assert model.left_bound == 0.0
    assert model.right_bound == 2.0
