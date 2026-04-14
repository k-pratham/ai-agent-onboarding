class AppBaseException(Exception):
    """Base exception isolating core app exceptions from arbitrary runtime errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseTransactionError(AppBaseException):
    """Raised when a generic SQLAlchemy commit/flush operation bounces."""
    pass

class CandidateNotFoundError(AppBaseException):
    """Raised when parsing queries pointing back against missing candidate objects."""
    pass

class ToolExecutionError(AppBaseException):
    """Raised when an MCP interaction routing breaks logic locally."""
    pass
