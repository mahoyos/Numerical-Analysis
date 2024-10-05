from pydantic import BaseModel
from typing import Union

class SumInput(BaseModel):
    num1: Union[int, float]
    num2: Union[int, float]