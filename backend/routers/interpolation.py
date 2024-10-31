from fastapi import APIRouter
from models.interpolation import (
    InterpolationInput
)
from services.interpolation import InterpolationService
from typing import Dict, Any

interpolation_router = APIRouter()


@interpolation_router.post("/interpolation")
async def systems_equations_route(input_data: InterpolationInput) -> Dict[str, Any]:
    method = input_data.method
    if method == "newton":
        result = InterpolationService.newton_interpolation(
            input_data.x_points,
            input_data.y_points,
            input_data.error_type,
        )

        result = {"polynom": str(result)}
    else:
        return {"error": "Invalid method specified."}
    return result
