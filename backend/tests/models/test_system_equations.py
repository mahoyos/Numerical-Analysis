import pytest
from pydantic import ValidationError

from models.system_equations import SystemsEquationsInput


def test_systems_equations_input_valid_data() -> None:
    model = SystemsEquationsInput(
        matrix_A=[[4, 1], [2, 3]],
        solution_vector=[1, 2],
        initial_guess=[0, 0],
        omega=1.1,
        tolerance=1e-6,
        max_iterations=100,
        error_type="absolute",
        method="jacobi",
    )
    assert model.method == "jacobi"


def test_systems_equations_input_invalid_method() -> None:
    with pytest.raises(ValidationError):
        SystemsEquationsInput(
            matrix_A=[[4, 1], [2, 3]],
            solution_vector=[1, 2],
            initial_guess=[0, 0],
            omega=1.1,
            tolerance=1e-6,
            max_iterations=100,
            error_type="absolute",
            method="invalid",
        )
