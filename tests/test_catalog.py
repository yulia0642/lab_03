import json
import pytest
from catalog import (
    Book,
    BookNotFoundError,
    Catalog,
    CorruptedFileError,
    DuplicateIDError,
    InvalidBookError,
    UnsupportedVersionError,
)
from catalog.storage import load_catalog, save_catalog


@pytest.fixture
def sample_books():
    return [
        Book("B001", "Преступление и наказание", "Роман", 1866, "Фёдор Достоевский", "978-5-17-090738-2"),
        Book("B002", "Война и мир", "Роман", 1869, "Лев Толстой", "5-17-090738-2"),
        Book("B003", "Капитанская дочка", "Повесть", 1836, "Александр Пушкин", "978-5-17-090738-2"),
    ]


def test_book_rejects_invalid_values():
    with pytest.raises(InvalidBookError):
        Book("", "Название", "Роман", 2000, "Автор", "978-5-17-090738-2")


def test_add_get_duplicate_remove(sample_books):
    catalog = Catalog()
    catalog.add(sample_books[0])
    assert catalog.get("B001") == sample_books[0]
    with pytest.raises(DuplicateIDError):
        catalog.add(sample_books[0])
    catalog.remove("B001")
    assert len(catalog) == 0
    with pytest.raises(BookNotFoundError):
        catalog.remove("B001")


def test_search_and_protocols(sample_books):
    catalog = Catalog()
    for book in sample_books:
        catalog.add(book)
    assert [book.book_id for book in catalog.find_by_category("РОМАН")] == ["B001", "B002"]
    assert [book.book_id for book in catalog.find_by_name("ВОЙНА")] == ["B002"]
    result = catalog.find_by_category("Роман")
    result.clear()
    assert len(catalog.find_by_category("Роман")) == 2
    assert len(catalog) == 3
    assert "B002" in catalog
    assert [book.book_id for book in catalog] == ["B001", "B002", "B003"]


def test_json_round_trip(tmp_path, sample_books):
    catalog = Catalog()
    for book in sample_books:
        catalog.add(book)
    file_path = tmp_path / "catalog.json"
    save_catalog(catalog, file_path)
    restored = Catalog()
    load_catalog(restored, file_path)
    assert list(restored) == sample_books


def test_failed_load_does_not_change_catalog(tmp_path, sample_books):
    catalog = Catalog()
    catalog.add(sample_books[0])
    file_path = tmp_path / "broken.json"
    file_path.write_text(
        json.dumps({"format_version": 1, "books": [
            {"book_id": "B002", "title": "Война и мир", "category": "Роман", "year": 1869,
             "author": "Лев Толстой", "isbn": "5-17-090738-2"},
            {"book_id": "B003", "title": "Сломанная запись", "category": "Роман", "year": "не год",
             "author": "Автор", "isbn": "978-5-17-090738-2"},
        ]}),
        encoding="utf-8",
    )
    with pytest.raises(CorruptedFileError):
        load_catalog(catalog, file_path)
    assert [book.book_id for book in catalog] == ["B001"]


def test_invalid_json_and_unknown_version(tmp_path):
    catalog = Catalog()
    file_path = tmp_path / "catalog.json"
    file_path.write_text("{broken", encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(catalog, file_path)
    file_path.write_text(json.dumps({"format_version": 99, "books": []}), encoding="utf-8")
    with pytest.raises(UnsupportedVersionError):
        load_catalog(catalog, file_path)