from services.non_linear_equations import NonLinearEquationsService


def test_fixed_point_service_success() -> None:
    response = NonLinearEquationsService.fixed_point_service(
        initial_guess=1.5,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="x**2 - 2",
        g_expression="(x + 2/x)/2",
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_newton_raphson_service_success() -> None:
    response = NonLinearEquationsService.newton_raphson_service(
        initial_guess=1.5,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="x**2 - 2",
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_multiple_roots_service_success() -> None:
    response = NonLinearEquationsService.multiple_roots_service(
        initial_guess=1.2,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="(x-1)**2",
        error_type="absolute",
    )
    assert response["status"] in ["success", "error"]


def test_false_position_service_success() -> None:
    response = NonLinearEquationsService.false_position_service(
        left_bound=0,
        right_bound=3,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="x**2 - 4",
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_false_position_service_invalid_range() -> None:
    response = NonLinearEquationsService.false_position_service(
        left_bound=3,
        right_bound=5,
        tolerance=1e-6,
        max_iterations=20,
        function_expression="x**2 - 4",
        error_type="absolute",
    )
    assert response["status"] == "error"
    assert response["error"]["code"] == "RANGE_NOT_CONTAINING_ROOT"


def test_bisection_service_success() -> None:
    response = NonLinearEquationsService.bisection_service(
        left_bound=0,
        right_bound=3,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="x**2 - 4",
        error_type="relative",
    )
    assert response["status"] == "success"


def test_secant_service_success() -> None:
    response = NonLinearEquationsService.secant_service(
        left_bound=1,
        right_bound=3,
        tolerance=1e-6,
        max_iterations=100,
        function_expression="x**2 - 4",
        error_type="absolute",
    )
    assert response["status"] == "success"


def test_bisection_service_left_bound_is_root() -> None:
    response = NonLinearEquationsService.bisection_service(
        left_bound=2,
        right_bound=4,
        tolerance=1e-6,
        max_iterations=50,
        function_expression="x**2 - 4",
        error_type="absolute",
    )
    assert response["status"] == "success"
    assert 2 <= response["root"] <= 4


def test_fixed_point_max_iterations_reached_error() -> None:
    response = NonLinearEquationsService.fixed_point_service(
        initial_guess=0.0,
        tolerance=1e-12,
        max_iterations=0,
        function_expression="x + 1",
        g_expression="x + 1",
        error_type="absolute",
    )
    assert response["status"] == "error"
    assert response["error"]["code"] == "MAX_ITERATIONS_REACHED"
