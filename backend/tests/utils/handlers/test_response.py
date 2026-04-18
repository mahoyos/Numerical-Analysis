from utils.errors.base_error import BaseError
from utils.handlers.response import ResponseHandler


def test_success_response_shape() -> None:
    response = ResponseHandler.success_response({"root": 1.0, "iterations": [[0, 1.0, 0.0, 0.0]]}, spectral_radius=0.5)
    assert response["status"] == "success"
    assert response["root"] == 1.0
    assert response["error"] is None
    assert response["spectral_radius"] == 0.5


def test_success_response_reads_spectral_radius_from_data() -> None:
    response = ResponseHandler.success_response({"root": [1.0], "iterations": [], "spectral_radius": 0.7})
    assert response["spectral_radius"] == 0.7


def test_error_response_shape() -> None:
    response = ResponseHandler.error_response(BaseError("bad", "BAD"))
    assert response["status"] == "error"
    assert response["error"]["code"] == "BAD"
    assert response["root"] is None
