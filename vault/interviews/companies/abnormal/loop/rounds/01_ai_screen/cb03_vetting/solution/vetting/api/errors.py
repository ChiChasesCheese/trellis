"""One error shape for the whole API: ``{"error": {"code": ..., "message": ...}}``."""
from __future__ import annotations

from vetting.errors import ConfigError, NotFoundError, ValidationError, VettingError


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status, self.code, self.message = status, code, message

    def body(self) -> dict:
        return {"error": {"code": self.code, "message": self.message}}


def from_exception(exc: VettingError) -> ApiError:
    if isinstance(exc, NotFoundError):
        return ApiError(404, "not_found", str(exc))
    if isinstance(exc, ValidationError):
        return ApiError(400, "invalid_request", str(exc))
    if isinstance(exc, ConfigError):
        return ApiError(500, "config_error", "server configuration error")
    return ApiError(500, "internal_error", "internal error")
