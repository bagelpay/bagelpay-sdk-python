"""BagelPay SDK Exceptions"""

from typing import Optional, Dict, Any


class BagelPayError(Exception):
    """Base exception for BagelPay SDK"""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class BagelPayAPIError(BagelPayError):
    """Exception raised when API returns an error response"""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        api_error: Optional['ApiError'] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.api_error = api_error
        super().__init__(message)
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.error_code:
            parts.append(f"Code: {self.error_code}")
        return " | ".join(parts)


class BagelPayAuthenticationError(BagelPayAPIError):
    """Exception raised for authentication errors"""
    pass


class BagelPayValidationError(BagelPayAPIError):
    """Exception raised for validation errors"""
    pass


class BagelPayNotFoundError(BagelPayAPIError):
    """Exception raised when resource is not found"""
    pass


class BagelPayRateLimitError(BagelPayAPIError):
    """Exception raised when rate limit is exceeded"""
    pass


class BagelPayServerError(BagelPayAPIError):
    """Exception raised for server errors (5xx)"""
    pass