from fastapi import APIRouter
from models.non_linear_equations import FixedPointInput
from services.non_linear_equations.fixed_point import FixedPointService
from typing import Dict, Any

router = APIRouter()


@router.post("/fixed-point")
async def fixed_point_route(input_data: FixedPointInput) -> Dict[str, Any]:
    result = FixedPointService.fixed_point_service(
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.function_expression,
        input_data.g_expression
    )
    print("RESULT : ", result["root"])
    return result
