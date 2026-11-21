class CatalogError(Exception):
    """Base class for catalog errors."""


class InvalidBookError(CatalogError):
    """Raised when a book contains invalid data."""


class DuplicateIDError(CatalogError):
    """Raised when a book ID is already present in the catalog."""


class BookNotFoundError(CatalogError):
    """Raised when a requested book ID is absent."""


class UnsupportedVersionError(CatalogError):
    """Raised when a JSON file uses an unsupported format version."""


class CorruptedFileError(CatalogError):
    """Raised when a catalog file is invalid or cannot be read."""