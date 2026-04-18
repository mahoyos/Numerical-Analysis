import pytest
from pydantic import ValidationError

from models.interpolation import InterpolationInput


def test_interpolation_input_valid_data() -> None:
    model = InterpolationInput(
        method="newton",
        x_points=[0, 1, 2],
        y_points=[1, 2, 5],
    )
    assert model.method == "newton"


def test_interpolation_input_invalid_method() -> None:
    with pytest.raises(ValidationError):
        InterpolationInput(
            method="bad",
            x_points=[0, 1],
            y_points=[1, 2],
        )
