import pytest


@pytest.mark.acceptance
def test_acceptance_non_linear_flow_returns_expected_root(client) -> None:
    payload = {
        "left_bound": 0,
        "right_bound": 3,
        "tolerance": 1e-8,
        "max_iterations": 100,
        "function_expression": "x**2 - 4",
        "error_type": "absolute",
    }

    response = client.post("/bisection", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert abs(body["root"] - 2.0) < 1e-3


@pytest.mark.acceptance
def test_acceptance_system_equations_flow_returns_vector_solution(client) -> None:
    payload = {
        "matrix_A": [[4.0, 1.0], [2.0, 3.0]],
        "solution_vector": [1.0, 2.0],
        "initial_guess": [0.0, 0.0],
        "omega": 1.1,
        "tolerance": 1e-6,
        "max_iterations": 100,
        "error_type": "absolute",
        "method": "gauss-seidel",
    }

    response = client.post("/systems-equations", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert isinstance(body["root"], list)
    assert len(body["root"]) == 2


@pytest.mark.acceptance
def test_acceptance_interpolation_flow_returns_polynomial(client) -> None:
    payload = {
        "method": "lagrange",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
    }

    response = client.post("/interpolation", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert "polynom" in body
    assert "x" in body["polynom"]
