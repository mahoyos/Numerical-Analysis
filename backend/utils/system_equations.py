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
