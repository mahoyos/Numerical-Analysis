def test_interpolation_newton_endpoint(client) -> None:
    payload = {
        "method": "newton",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
    }
    response = client.post("/interpolation", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert "polynom" in body


def test_interpolation_spline_endpoint(client) -> None:
    payload = {
        "method": "spline",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
        "degree": 1,
    }
    response = client.post("/interpolation", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert "polynom" in body


def test_interpolation_lagrange_endpoint(client) -> None:
    payload = {
        "method": "lagrange",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
    }
    response = client.post("/interpolation", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert "polynom" in body


def test_interpolation_vandermonde_endpoint(client) -> None:
    payload = {
        "method": "vandermonde",
        "x_points": [0, 1, 2],
        "y_points": [1, 2, 5],
    }
    response = client.post("/interpolation", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert "polynom" in body
