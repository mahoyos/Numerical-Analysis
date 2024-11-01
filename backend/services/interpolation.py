from typing import Dict, Any, List
import numpy as np
import sympy as sp


class InterpolationService:
    @staticmethod
    def newton_service(x_points: List, y_points: List, error_type: str):
        n = len(x_points)

        divided_difference_table = np.zeros((n, n + 1))

        divided_difference_table[:, 0] = x_points
        divided_difference_table[:, 1] = y_points

        for j in range(2, n + 1):
            for i in range(j - 1, n):
                divided_difference_table[i, j] = (divided_difference_table[i, j - 1] - divided_difference_table[i - 1, j - 1]) / (divided_difference_table[i, 0] - divided_difference_table[i - j + 1, 0])

        coefficients = divided_difference_table[np.arange(n), np.arange(1, n + 1)]

        x_sym = sp.symbols('x')
        polinom = coefficients[0]
        product = 1

        for i in range(1, n):
            product *= (x_sym - x_points[i - 1])
            polinom += coefficients[i] * product

        polinom = sp.simplify(polinom)

        return polinom
