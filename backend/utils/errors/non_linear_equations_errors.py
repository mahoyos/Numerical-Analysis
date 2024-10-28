from utils.errors.base_error import BaseError


class FalsePositionErrors(BaseError):
    def __init__(self, message: str, error_code: str):
        super().__init__(message, error_code)

    class RangeNotContainingRootError(BaseError):
        def __init__(self, message: str = "The initial range does not contain the root."):
            super().__init__(message, "RANGE_NOT_CONTAINING_ROOT")
