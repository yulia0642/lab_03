from catalog import Book, Catalog


def main() -> None:
    catalog = Catalog()

    books = [
        Book(
            book_id="B001",
            title="Преступление и наказание",
            category="Роман",
            year=1866,
            author="Фёдор Достоевский",
            isbn="ISBN-13: 978-5-17-090738-2",
        ),
        Book(
            book_id="B002",
            title="Война и мир",
            category="Роман",
            year=1869,
            author="Лев Толстой",
            isbn="5-17-090738-2",
        ),
        Book(
            book_id="B003",
            title="Капитанская дочка",
            category="Повесть",
            year=1836,
            author="Александр Пушкин",
            isbn="978-5-17-090738-2",
        ),
    ]

    for book in books:
        catalog.add(book)

    print("Все книги каталога:")
    for book in catalog:
        print(book)

    print("\nПоиск книги по ID B002:")
    print(catalog.get("B002"))

    print("\nКниги категории «Роман»:")
    for book in catalog.find_by_category("Роман"):
        print(book.title)

    print("\nПоиск по названию «война»:")
    for book in catalog.find_by_name("война"):
        print(book.title)

    catalog.save("books.json")
    print("\nКаталог сохранён в books.json")

    restored_catalog = Catalog()
    restored_catalog.load("books.json")
    print(f"Загружено книг: {len(restored_catalog)}")


if __name__ == "__main__":
    main()
