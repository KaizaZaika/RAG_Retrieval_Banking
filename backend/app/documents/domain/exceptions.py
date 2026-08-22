class DocumentError(Exception):
    """Base exception for document-related domain errors."""
class DocumentNotFoundError(Exception):
    pass


class DocumentParsingError(Exception):
    pass
