class ProcessingError(Exception):
    """Base exception for business logic errors."""
    pass

class InvalidInputError(ProcessingError):
    pass

class NoSpeechDetectedError(ProcessingError):
    pass
