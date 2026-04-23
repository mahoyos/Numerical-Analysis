import pytest


@pytest.mark.smoke
def test_health_endpoint_is_up(client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.smoke
def test_bisection_endpoint_smoke(client) -> None:
    payload = {
        "left_bound": 0,
        "right_bound": 3,
        "tolerance": 1e-6,
        "max_iterations": 100,
        "function_expression": "x**2 - 4",
        "error_type": "absolute",
    }

    response = client.post("/bisection", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert "root" in body


@pytest.mark.smoke
def test_interpolation_endpoint_smoke(client) -> None:
    payload = {
        "method": "newton",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
    }

    response = client.post("/interpolation", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert "polynom" in body
