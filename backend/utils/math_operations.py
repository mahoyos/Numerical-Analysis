import sympy as sp

class MathOperations:
    @staticmethod
    def evaluate_function(
        function : str,
        point : float
    ) -> float:
        x = sp.symbols('x')
        function = sp.sympify(function)
        return float(function.evalf(subs={x: point}))

    @staticmethod
    def get_derivative(function : str) -> str:
        x = sp.symbols('x')
        function = sp.sympify(function)
        return sp.diff(function, x)
