def test_systems_equations_jacobi_endpoint(client) -> None:
    payload = {
        "matrix_A": [[10.0, 0.0], [0.0, 5.0]],
        "solution_vector": [20.0, 15.0],
        "initial_guess": [0.0, 0.0],
        "omega": 1.1,
        "tolerance": 1e-6,
        "max_iterations": 50,
        "error_type": "absolute",
        "method": "jacobi",
    }
    response = client.post("/systems-equations", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"


def test_systems_equations_gauss_seidel_endpoint(client) -> None:
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


def test_systems_equations_sor_endpoint(client) -> None:
    payload = {
        "matrix_A": [[4.0, 1.0], [2.0, 3.0]],
        "solution_vector": [1.0, 2.0],
        "initial_guess": [0.0, 0.0],
        "omega": 1.1,
        "tolerance": 1e-6,
        "max_iterations": 200,
        "error_type": "absolute",
        "method": "sor",
    }
    response = client.post("/systems-equations", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"
