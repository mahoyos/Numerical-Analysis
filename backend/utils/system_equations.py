from typing import Dict, Any
import numpy as np


class SystemEquationsUtils:
    @staticmethod
    def verify_solution(matrix: np.ndarray, solution: np.ndarray, vector: np.ndarray, tolerance: float) -> Dict[str, Any]:
        residual = np.linalg.norm(np.dot(matrix, solution) - vector)
        convergence_status = "converged" if residual < tolerance else "not_converged"

        return {
            "residual": float(residual),
            "status": convergence_status
        }

    @staticmethod
    def spectral_radius(
        matrix_A: np.ndarray,
        method: str,
        omega: float = 1.0
    ) -> float:
        if method == "jacobi":
            D = np.diag(np.diag(matrix_A))
            L = np.tril(matrix_A, k=-1)
            U = np.triu(matrix_A, k=1)

            T_j = np.linalg.inv(D) @ (L + U)
            eigenvalues = np.linalg.eigvals(T_j)
            spectral_radius = max(abs(eigenvalues))

            return spectral_radius
        elif method == "sor":
            D = np.diag(np.diag(matrix_A))
            L = np.tril(matrix_A, k=-1)
            U = np.triu(matrix_A, k=1)

            T_sor = np.linalg.inv(D + omega * L).dot((1 - omega) * D - omega * U)
            eigenvalues = np.linalg.eigvals(T_sor)
            spectral_radius = max(abs(eigenvalues))

            return spectral_radius
        elif method == "gauss_seidel":
            D = np.diag(np.diag(matrix_A))
            L = np.tril(matrix_A, k=-1)
            U = np.triu(matrix_A, k=1)

            T_gs = -(np.linalg.inv(D + L)).dot(U)
            eigenvalues = np.linalg.eigvals(T_gs)
            spectral_radius = max(abs(eigenvalues))

            return spectral_radius
