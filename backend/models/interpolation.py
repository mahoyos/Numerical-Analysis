from pydantic import BaseModel, Field
from typing import Literal, List, Optional


class InterpolationInput(BaseModel):
    x_points: List[float]
    y_points: List[float]
    error_type: Literal['absolute', 'relative']
    method: Literal['newton', 'spline']
    degree: Optional[int]
