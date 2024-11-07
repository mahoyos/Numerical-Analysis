from pydantic import BaseModel
from typing import Literal, List, Optional


class InterpolationInput(BaseModel):
    method: Literal['newton', 'spline']
    x_points: List[float]
    y_points: List[float]
    degree: Optional[int] = None
