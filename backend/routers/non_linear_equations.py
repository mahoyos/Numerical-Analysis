from fastapi import APIRouter
from models.non_linear_equations import FixedPointInput, FalsePositionInput
from backend.services.non_linear_equations import NonLinearEquationsService as NonLinearEquations
from typing import Dict, Any

router = APIRouter()


@router.post("/fixed-point")
async def fixed_point_route(input_data: FixedPointInput) -> Dict[str, Any]:
    result = NonLinearEquations.fixed_point_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.g_expression
    )
    return result


@router.post("/false-position")
async def false_position_route(input_data: FalsePositionInput) -> Dict[str, Any]:
    result = NonLinearEquations.false_position_service(
        input_data.left_bound,
        input_data.right_bound,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression
    )
    return result
