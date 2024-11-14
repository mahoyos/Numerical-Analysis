import numpy as np
from typing import List

class SystemEquationsUtils:
    @staticmethod
    def spectral_radius(
        matrix_A: List[List[float]]
    ) -> float:
        eigenvalues = np.linalg.eigvals(matrix_A)
        spectral_radius = max(abs(eigenvalues))
        return spectral_radius