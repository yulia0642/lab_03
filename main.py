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
            isbn="978-5-17-090738-2",
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

    print("All books in the catalog:")
    for book in catalog:
        print(book)

    print("\nBook with ID B002:")
    print(catalog.get("B002"))

    print("\nBooks in the 'Novel' category:")
    for book in catalog.find_by_category("Роман"):
        print(book.title)

    print("\nSearch results for 'war':")
    for book in catalog.find_by_name("война"):
        print(book.title)

    catalog.save("books.json")
    print("\nCatalog saved to books.json")

    restored_catalog = Catalog()
    restored_catalog.load("books.json")
    print(f"Number of books loaded: {len(restored_catalog)}")


if __name__ == "__main__":
    main()