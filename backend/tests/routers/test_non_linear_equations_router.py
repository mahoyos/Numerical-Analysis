def test_bisection_endpoint(client) -> None:
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


def test_false_position_endpoint_error(client) -> None:
    payload = {
        "left_bound": 3,
        "right_bound": 5,
        "tolerance": 1e-6,
        "max_iterations": 50,
        "function_expression": "x**2 - 4",
        "error_type": "absolute",
    }
    response = client.post("/false-position", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "error"


def test_fixed_point_endpoint(client) -> None:
    payload = {
        "initial_guess": 1.5,
        "tolerance": 1e-6,
        "max_iterations": 100,
        "function_expression": "x**2 - 2",
        "g_expression": "(x + 2/x)/2",
        "error_type": "relative",
    }
    response = client.post("/fixed-point", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"


def test_newton_raphson_endpoint(client) -> None:
    payload = {
        "initial_guess": 1.5,
        "tolerance": 1e-6,
        "max_iterations": 100,
        "function_expression": "x**2 - 2",
        "error_type": "absolute",
    }
    response = client.post("/newton-raphson", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"


def test_secant_endpoint(client) -> None:
    payload = {
        "left_bound": 1,
        "right_bound": 3,
        "tolerance": 1e-6,
        "max_iterations": 100,
        "function_expression": "x**2 - 4",
        "error_type": "absolute",
    }
    response = client.post("/secant", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"
