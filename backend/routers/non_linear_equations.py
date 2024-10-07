from fastapi import APIRouter
from models.non_linear_equations import FixedPointInput, NewtonRaphsonInput
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
        input_data.g_expression
    )
    return result

@router.post("/newton-raphson")
async def newton_raphson_route(input_data: NewtonRaphsonInput) -> Dict[str, Any]:
    result = NonLinearEquationsService.newton_raphson_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression
    )
    return result