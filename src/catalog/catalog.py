from catalog.exceptions import BookNotFoundError, DuplicateIDError, InvalidBookError
from catalog.models import Book


class Catalog:
    """Stores books in insertion order and indexes them by ID and category."""

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}
        self._categories: dict[str, list[str]] = {}

    def add(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise InvalidBookError("Catalog allow add only Book objects")

        if book.book_id in self._books:
            raise DuplicateIDError(f"Book with ID {book.book_id} allready exist")

        self._books[book.book_id] = book
        category_key = book.category.lower()
        if category_key not in self._categories:
            self._categories[category_key] = []
        self._categories[category_key].append(book.book_id)

    def get(self, book_id: str) -> Book:
        if book_id not in self._books:
            raise BookNotFoundError(f"Book with ID {book_id} not found")
        return self._books[book_id]

    def remove(self, book_id: str) -> None:
        book = self.get(book_id)
        del self._books[book_id]

        category_key = book.category.lower()
        self._categories[category_key].remove(book_id)
        if not self._categories[category_key]:
            del self._categories[category_key]

    def find_by_category(self, category: str) -> list[Book]:
        book_ids = self._categories.get(category.lower(), [])
        return [self._books[book_id] for book_id in book_ids]

    def find_by_name(self, search_text: str) -> list[Book]:
        normalized_search_text = search_text.lower()
        return [book for book in self._books.values() if normalized_search_text in book.title.lower()]

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self):
        return iter(self._books.values())

    def __contains__(self, item_id: object) -> bool:
        return item_id in self._books

    def _replace_data(self, books: dict[str, Book], categories: dict[str, list[str]]) -> None:
        self._books = books
        self._categories = categories

    def save(self, file_path: str) -> None:
        from catalog.storage import save_catalog
        save_catalog(self, file_path)

    def load(self, file_path: str) -> None:
        from catalog.storage import load_catalog

        load_catalog(self, file_path)