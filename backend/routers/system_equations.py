from fastapi import APIRouter
from models.system_equations import (
    SystemsEquationsInput
)
from services.system_equations import SystemEquationsService
from typing import Dict, Any

system_equations_router = APIRouter()


@system_equations_router.post("/systems-equations")
async def systems_equations_route(input_data: SystemsEquationsInput) -> Dict[str, Any]:
    method = input_data.method
    if method == "sor":
        result = SystemEquationsService.sor_service(
            input_data.matrix_A,
            input_data.solution_vector,
            input_data.initial_guess,
            input_data.tolerance,
            input_data.max_iterations,
            input_data.omega,
            input_data.error_type,
        )
    elif method == "gauss-seidel":
        result = SystemEquationsService.gauss_seidel_service(
            input_data.matrix_A,
            input_data.solution_vector,
            input_data.initial_guess,
            input_data.tolerance,
            input_data.max_iterations,
            input_data.error_type,
        )
    elif method == "jacobi":
        result = SystemEquationsService.jacobi_service(
            input_data.matrix_A,
            input_data.solution_vector,
            input_data.initial_guess,
            input_data.tolerance,
            input_data.max_iterations,
            input_data.error_type,
        )
    else:
        return {"error": "Invalid method specified."}
    return result
