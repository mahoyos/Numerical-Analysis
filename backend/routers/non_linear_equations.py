from fastapi import APIRouter
from models.non_linear_equations import (
    FixedPointInput, 
    MultipleRootsInput, 
    NewtonRaphsonInput, 
    FalsePositionInput, 
    BisectionInput
)
from services.non_linear_equations import NonLinearEquationsService
from typing import Dict, Any

router = APIRouter()


@router.post("/fixed-point")
async def fixed_point_route(input_data: FixedPointInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.fixed_point_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.g_expression,
        input_data.error_type
    )
    return result


@router.post("/newton-raphson")
async def newton_raphson_route(input_data: NewtonRaphsonInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.newton_raphson_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.error_type
    )
    return result


@router.post("/multiple-roots")
async def multiple_roots_route(input_data: MultipleRootsInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.multiple_roots_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.error_type
    )
    return result


@router.post("/false-position")
async def false_position_route(input_data: FalsePositionInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.false_position_service(
        input_data.left_bound,
        input_data.right_bound,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.error_type
    )
    return result


@router.post("/bisection")
async def bisection_route(input_data: BisectionInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.bisection_service(
        input_data.left_bound,
        input_data.right_bound,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.error_type
    )
    return result