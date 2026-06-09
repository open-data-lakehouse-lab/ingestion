class ConnectorError(Exception):
    """Base exception for connector errors."""
    pass

class ConnectorConfigurationError(ConnectorError):
    """Raised when connector configuration is invalid or missing."""
    pass

class ConnectorHttpError(ConnectorError):
    """Raised when an HTTP error occurs."""
    pass

class ConnectorTimeoutError(ConnectorHttpError):
    """Raised when an HTTP request times out."""
    pass

class ConnectorInvalidResponseError(ConnectorError):
    """Raised when the response format is invalid (e.g. invalid JSON)."""
    pass
