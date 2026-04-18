import numpy as np

from utils.system_equations import SystemEquationsUtils


def test_verify_solution_converged() -> None:
    matrix = np.array([[2.0, 0.0], [0.0, 2.0]])
    solution = np.array([1.0, 1.0])
    vector = np.array([2.0, 2.0])
    result = SystemEquationsUtils.verify_solution(matrix, solution, vector, 1e-8)
    assert result["status"] == "converged"


def test_verify_solution_not_converged() -> None:
    matrix = np.array([[2.0, 0.0], [0.0, 2.0]])
    solution = np.array([0.0, 0.0])
    vector = np.array([2.0, 2.0])
    result = SystemEquationsUtils.verify_solution(matrix, solution, vector, 1e-8)
    assert result["status"] == "not_converged"


def test_spectral_radius_for_jacobi() -> None:
    matrix = np.array([[4.0, 1.0], [1.0, 3.0]])
    rho = SystemEquationsUtils.spectral_radius(matrix, "jacobi")
    assert rho >= 0


def test_spectral_radius_for_sor() -> None:
    matrix = np.array([[4.0, 1.0], [1.0, 3.0]])
    rho = SystemEquationsUtils.spectral_radius(matrix, "sor", omega=1.1)
    assert rho >= 0


def test_spectral_radius_for_gauss_seidel() -> None:
    matrix = np.array([[4.0, 1.0], [1.0, 3.0]])
    rho = SystemEquationsUtils.spectral_radius(matrix, "gauss_seidel")
    assert rho >= 0
