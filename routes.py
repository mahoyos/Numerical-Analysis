from fastapi import APIRouter
from models import SumInput  
from typing import Union

router = APIRouter()

@router.post("/sum")
async def sum_numbers(data: SumInput):
    result = data.num1 + data.num2
    return {"result": result}
