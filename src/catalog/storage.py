import json
from dataclasses import asdict
from pathlib import Path

from catalog.catalog import Catalog
from catalog.exceptions import (CatalogError, CorruptedFileError, DuplicateIDError, UnsupportedVersionError)
from catalog.models import Book


FORMAT_VERSION = 1


def save_catalog(catalog: Catalog, file_path: str | Path) -> None:
    data = {
        "format_version": FORMAT_VERSION,
        "books": [asdict(book) for book in catalog],
    }

    try:
        with Path(file_path).open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError as error:
        raise CorruptedFileError(f"Failed to save catalog file: {error}") from error


def load_catalog(catalog: Catalog, file_path: str | Path) -> None:
    """Load all data first; change the catalog only after full validation."""
    try:
        with Path(file_path).open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as error:
        raise CorruptedFileError(f"Failed to read catalog file: {error}") from error

    if not isinstance(data, dict) or "format_version" not in data or "books" not in data:
        raise CorruptedFileError("Invalid catalog file structure")

    if data["format_version"] != FORMAT_VERSION:
        raise UnsupportedVersionError(
            f"Format version {data['format_version']} is not supported"
        )

    if not isinstance(data["books"], list):
        raise CorruptedFileError("The 'books' field must contain a list")

    new_books: dict[str, Book] = {}
    new_categories: dict[str, list[str]] = {}

    try:
        for book_data in data["books"]:
            if not isinstance(book_data, dict):
                raise CorruptedFileError("Each book record must be an object")

            book = Book(**book_data)

            if book.book_id in new_books:
                raise DuplicateIDError(f"Duplicate book ID: {book.book_id}")

            new_books[book.book_id] = book

            category_key = book.category.lower()
            if category_key not in new_categories:
                new_categories[category_key] = []
            new_categories[category_key].append(book.book_id)

    except (CatalogError, TypeError, KeyError, ValueError) as error:
        raise CorruptedFileError(f"Invalid book data: {error}") from error

    catalog._replace_data(new_books, new_categories)