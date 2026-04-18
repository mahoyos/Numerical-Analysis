from services.interpolation import InterpolationService


def test_newton_service_builds_polynomial() -> None:
    poly = InterpolationService.newton_service([0, 1, 2], [1, 2, 5])
    assert "x" in str(poly)


def test_lagrange_service_builds_polynomial() -> None:
    poly = InterpolationService.lagrange_service([0, 1, 2], [1, 2, 5])
    assert "x" in str(poly)


def test_vandermonde_service_builds_polynomial() -> None:
    poly = InterpolationService.vandermonde_service([0, 1, 2], [1, 2, 5])
    assert "x" in str(poly)


def test_spline_service_returns_segments() -> None:
    segments = InterpolationService.spline_service([0, 1, 2], [1, 2, 5], 1)
    assert len(segments) == 2


def test_spline_service_degree_two_returns_segments() -> None:
    segments = InterpolationService.spline_service([0, 1, 2], [1, 2, 5], 2)
    assert len(segments) == 2
