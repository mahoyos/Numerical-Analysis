from typing import List
import numpy as np
import sympy as sp


class InterpolationService:
    @staticmethod
    def newton_service(x_points: List, y_points: List):
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

    @staticmethod
    def spline_service(x_points: List, y_points: List, degree: int):
        num_points = len(x_points)
        system_matrix = np.zeros(((degree + 1) * (num_points - 1), (degree + 1) * (num_points - 1)))
        solution_vector = np.zeros((degree + 1) * (num_points - 1))

        if degree == 1:
            row_index = 0
            for i in range(num_points - 1):
                system_matrix[row_index, i * 2] = x_points[i]
                system_matrix[row_index, i * 2 + 1] = 1
                solution_vector[row_index] = y_points[i]
                row_index += 1

            for i in range(1, num_points):
                system_matrix[row_index, (i - 1) * 2] = x_points[i]
                system_matrix[row_index, (i - 1) * 2 + 1] = 1
                solution_vector[row_index] = y_points[i]
                row_index += 1

        elif degree == 2:
            row_index = 0
            squared_x_points = np.array(x_points) ** 2

            for i in range(num_points - 1):
                system_matrix[row_index, i * 3] = squared_x_points[i]
                system_matrix[row_index, i * 3 + 1] = x_points[i]
                system_matrix[row_index, i * 3 + 2] = 1
                solution_vector[row_index] = y_points[i]
                row_index += 1

            for i in range(1, num_points):
                system_matrix[row_index, (i - 1) * 3] = squared_x_points[i]
                system_matrix[row_index, (i - 1) * 3 + 1] = x_points[i]
                system_matrix[row_index, (i - 1) * 3 + 2] = 1
                solution_vector[row_index] = y_points[i]
                row_index += 1

            for i in range(1, num_points - 1):
                system_matrix[row_index, (i - 1) * 3] = 2 * x_points[i]
                system_matrix[row_index, (i - 1) * 3 + 1] = 1
                system_matrix[row_index, i * 3] = -2 * x_points[i]
                system_matrix[row_index, i * 3 + 1] = -1
                solution_vector[row_index] = 0
                row_index += 1

            system_matrix[row_index, 0] = 2
            solution_vector[row_index] = 0

        coefficients = np.linalg.solve(system_matrix, solution_vector)
        coefficients = np.where(np.abs(coefficients) < 1e-10, 0, coefficients)

        coefficients_table = coefficients.reshape((num_points - 1, degree + 1))
        return coefficients_table

    @staticmethod
    def vandermonde_service(x_points: List[float], y_points: List[float]):
        n = len(x_points)
        A = np.vander(x_points, n)
        coefficients = np.linalg.solve(A, y_points)
        x_sym = sp.symbols('x')
        polinom = sum(c * x_sym**i for i, c in enumerate(reversed(coefficients)))
        polinom = sp.simplify(polinom)
        return polinom

    @staticmethod
    def lagrange_service(x_points: List[float], y_points: List[float]):
        x = sp.symbols('x')
        polinom = 0
        n = len(x_points)

        for i in range(n):
            L_i = 1

            for j in range(n):

                if i != j:
                    L_i *= (x - x_points[j]) / (x_points[i] - x_points[j])
            polinom += y_points[i] * L_i

        polinom = sp.simplify(polinom)
        return polinom
