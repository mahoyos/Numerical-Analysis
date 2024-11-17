from typing import Any, Dict
from utils.errors.base_error import BaseError


class ResponseHandler:
    @staticmethod
    def success_response(data: Any, **additional_fields: Any) -> Dict[str, Any]:
        response = {
            "status": "success",
            "root": data["root"],
            "iterations": data["iterations"],
            "error": None,
            **additional_fields
        }

        # Añadir spectral_radius solo si existe en data
        if "spectral_radius" in data:
            response["spectral_radius"] = data["spectral_radius"]

        return response

    @staticmethod
    def error_response(error: BaseError) -> Dict[str, Any]:
        return {
            "status": "error",
            "root": None,
            "iterations": None,
            "error": {
                "code": error.error_code,
                "message": error.message
            }
        }
