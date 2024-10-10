from typing import Any, Dict
from utils.errors.base_error import BaseError


class ResponseHandler:
    @staticmethod
    def success_response(data: Any) -> Dict[str, Any] :
        return {
            "status" : "success",
            "root" : data["root"],
            "iterations" : data["iterations"],
            "error" : None
        }

    @staticmethod
    def error_response(error : BaseError) -> Dict[str, Any] :
        return {
            "status" : "error",
            "root" : None,
            "iterations" : None,
            "error" : {
                "code" : error.error_code,
                "message" : error.message
            }
        }