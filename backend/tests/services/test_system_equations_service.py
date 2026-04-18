from services.system_equations import SystemEquationsService


MATRIX = [[4.0, 1.0], [2.0, 3.0]]
VECTOR = [1.0, 2.0]
INITIAL = [0.0, 0.0]
JACOBI_MATRIX = [[10.0, 0.0], [0.0, 5.0]]
JACOBI_VECTOR = [20.0, 15.0]


def test_jacobi_service_success() -> None:
    response = SystemEquationsService.jacobi_service(
        matrix_A=JACOBI_MATRIX,
        solution_vector=JACOBI_VECTOR,
        initial_guess=INITIAL,
        tolerance=1e-6,
        max_iterations=50,
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_gauss_seidel_service_success() -> None:
    response = SystemEquationsService.gauss_seidel_service(
        matrix_A=MATRIX,
        solution_vector=VECTOR,
        initial_guess=INITIAL,
        tolerance=1e-6,
        max_iterations=100,
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_sor_service_success() -> None:
    response = SystemEquationsService.sor_service(
        matrix_A=MATRIX,
        solution_vector=VECTOR,
        initial_guess=INITIAL,
        tolerance=1e-6,
        max_iterations=200,
        omega=1.1,
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_sor_service_invalid_matrix_errors() -> None:
    response = SystemEquationsService.sor_service(
        matrix_A=[[0.0, 0.0], [0.0, 0.0]],
        solution_vector=VECTOR,
        initial_guess=INITIAL,
        tolerance=1e-6,
        max_iterations=10,
        omega=1.1,
        error_type="absolute",
    )
    assert response["status"] == "error"
