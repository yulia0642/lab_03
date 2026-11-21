from dataclasses import dataclass
from catalog.exceptions import InvalidBookError


def _normalize_isbn(isbn: str) -> str:
    value = isbn.strip()
    return value.replace("-", "").replace(" ", "")


def _is_valid_isbn(isbn: str) -> bool:
    value = _normalize_isbn(isbn)
    isbn_10 = (
        len(value) == 10
        and value[:9].isdigit()
        and (value[9].isdigit() or value[9] == "X")
    )
    isbn_13 = len(value) == 13 and value.isdigit()
    return isbn_10 or isbn_13


@dataclass
class Book:
    book_id: str
    title: str
    category: str
    year: int
    author: str
    isbn: str

    def __post_init__(self) -> None:
        if not isinstance(self.book_id, str) or not self.book_id.strip():
            raise InvalidBookError("Invalid book ID")

        if not isinstance(self.title, str) or not self.title.strip():
            raise InvalidBookError("Book title cannot be empty")

        if not isinstance(self.category, str) or not self.category.strip():
            raise InvalidBookError("Book category cannot be empty")

        if type(self.year) is not int or self.year <= 0:
            raise InvalidBookError("Publication year must be a positive integer")

        if not isinstance(self.author, str) or not self.author.strip():
            raise InvalidBookError("Author cannot be empty")

        if not isinstance(self.isbn, str) or not _is_valid_isbn(self.isbn):
            raise InvalidBookError("Invalid ISBN")