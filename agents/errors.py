"""Enterprise-grade error handling and exceptions."""

import logging
from typing import Any, Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """Error severity levels."""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ErrorCode(str, Enum):
    """Standardized error codes."""
    # Validation errors
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_QUERY = "INVALID_QUERY"
    INVALID_ANSWER = "INVALID_ANSWER"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
    
    # API errors
    API_FAILURE = "API_FAILURE"
    API_TIMEOUT = "API_TIMEOUT"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    
    # Processing errors
    JSON_PARSE_ERROR = "JSON_PARSE_ERROR"
    EVALUATION_FAILED = "EVALUATION_FAILED"
    GENERATION_FAILED = "GENERATION_FAILED"
    REFINEMENT_FAILED = "REFINEMENT_FAILED"
    
    # System errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"


class AeruliasException(Exception):
    """Base exception for Aerulias AI."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.details = details or {}
        self.user_message = user_message or "An error occurred processing your request"
        
        super().__init__(self.message)
        
        # Log the exception
        log_level = {
            ErrorSeverity.CRITICAL: logging.CRITICAL,
            ErrorSeverity.ERROR: logging.ERROR,
            ErrorSeverity.WARNING: logging.WARNING,
            ErrorSeverity.INFO: logging.INFO,
        }[severity]
        
        logger.log(
            log_level,
            f"{error_code}: {message}",
            extra={"details": self.details}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "error": self.error_code.value,
            "message": self.user_message,
            "severity": self.severity.value,
            "details": self.details if self.severity in [
                ErrorSeverity.CRITICAL, ErrorSeverity.ERROR
            ] else {}
        }


class ValidationError(AeruliasException):
    """Validation-related error."""
    
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_INPUT,
            severity=ErrorSeverity.WARNING,
            details=details,
            **kwargs
        )


class QueryValidationError(ValidationError):
    """Query validation error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_QUERY,
            field="query",
            **kwargs
        )


class AnswerValidationError(ValidationError):
    """Answer validation error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_ANSWER,
            field="answer",
            **kwargs
        )


class APIError(AeruliasException):
    """API-related error."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.API_FAILURE,
        status_code: Optional[int] = None,
        **kwargs
    ):
        details = {"status_code": status_code} if status_code else {}
        super().__init__(
            message=message,
            error_code=error_code,
            severity=ErrorSeverity.ERROR,
            details=details,
            user_message="External API error occurred",
            **kwargs
        )


class TimeoutError(APIError):
    """API timeout error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.API_TIMEOUT,
            user_message="Request timeout - please try again",
            **kwargs
        )


class RateLimitError(APIError):
    """Rate limit exceeded error."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        details = {"retry_after_seconds": retry_after} if retry_after else {}
        super().__init__(
            message=message,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            user_message="Service is busy - please try again later",
            **kwargs
        )


class ProcessingError(AeruliasException):
    """Processing-related error."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        operation: Optional[str] = None,
        **kwargs
    ):
        details = {"operation": operation} if operation else {}
        super().__init__(
            message=message,
            error_code=error_code,
            severity=ErrorSeverity.ERROR,
            details=details,
            user_message="Error processing request",
            **kwargs
        )


class EvaluationError(ProcessingError):
    """Evaluation-specific error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.EVALUATION_FAILED,
            operation="evaluation",
            **kwargs
        )


class GenerationError(ProcessingError):
    """Generation-specific error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.GENERATION_FAILED,
            operation="generation",
            **kwargs
        )


class RefinementError(ProcessingError):
    """Refinement-specific error."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code=ErrorCode.REFINEMENT_FAILED,
            operation="refinement",
            **kwargs
        )


def handle_error(
    exception: Exception,
    context: Optional[Dict[str, Any]] = None,
    default_error_code: ErrorCode = ErrorCode.INTERNAL_ERROR
) -> AeruliasException:
    """Convert any exception to AeruliasException with proper context."""
    if isinstance(exception, AeruliasException):
        return exception
    
    context = context or {}
    
    # Map common exceptions
    exception_mapping = {
        ValueError: ErrorCode.INVALID_INPUT,
        TypeError: ErrorCode.INVALID_INPUT,
        KeyError: ErrorCode.MISSING_REQUIRED_FIELD,
        TimeoutError: ErrorCode.API_TIMEOUT,
    }
    
    error_code = exception_mapping.get(type(exception), default_error_code)
    
    return AeruliasException(
        message=str(exception),
        error_code=error_code,
        severity=ErrorSeverity.ERROR,
        details=context,
        user_message="An unexpected error occurred"
    )


def create_error_response(
    error: Exception,
    status_code: int = 500
) -> Dict[str, Any]:
    """Create a standardized error response."""
    if isinstance(error, AeruliasException):
        exception = error
    else:
        exception = handle_error(error)
    
    return {
        "success": False,
        "error": exception.to_dict(),
        "status_code": status_code
    }
