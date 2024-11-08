from fastapi import APIRouter
from models.interpolation import (
    InterpolationInput
)
from services.interpolation import InterpolationService
from typing import Dict, Any

interpolation_router = APIRouter()


@interpolation_router.post("/interpolation")
async def interpolation_route(input_data: InterpolationInput) -> Dict[str, Any]:
    method = input_data.method
    if method == "newton":
        result = InterpolationService.newton_service(
            input_data.x_points,
            input_data.y_points,
        )

        result = {"polynom": str(result)}
    elif method == "spline":
        result = InterpolationService.spline_service(
            input_data.x_points,
            input_data.y_points,
            input_data.degree,
        )

        result = {"polynom": str(result)}
    elif method == "vandermonde":
        result = InterpolationService.vandermonde_service(
            input_data.x_points,
            input_data.y_points,
        )
    elif method == "lagrange":
        result = InterpolationService.lagrange_service(
            input_data.x_points,
            input_data.y_points,
        )
    else:
        return {"error": "Invalid method specified."}
    return result
