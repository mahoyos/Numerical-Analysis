from fastapi import APIRouter
from models.system_equations import (
    SorInput,
)
from services.system_equations import SystemEquationsService
from typing import Dict, Any

system_equations_router = APIRouter()


@system_equations_router.post("/sor")
async def sor_route(input_data: SorInput) -> Dict[str, Any]:
    result = SystemEquationsService.sor_service(
        input_data.matrix_A,
        input_data.solution_vector,
        input_data.initial_guess,
        input_data.tolerance,
        input_data.max_iterations,
        input_data.omega,
        input_data.error_type,
    )
    return result
