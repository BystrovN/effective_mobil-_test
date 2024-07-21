from objects.book import Book
from database import Database


class Library:
    """Класс для управления книгами в библиотеке."""

    def __init__(self, database: Database) -> None:
        self.db = database

    def _get_book_by_id(self, book_id: str) -> Book | None:
        """Поиск книги по переданному id."""
        search = self.db.find_by('id', book_id)
        if not search:
            return

        return Book(**search[0])

    def get_all_books(self) -> list[Book]:
        """Все книги."""
        return [Book(**book_data) for book_data in self.db.data]

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавить новую книгу."""
        book = Book(title, author, year)
        self.db.append_data(book.__dict__)
        return book

    def delete_book(self, book_id: str) -> Book | None:
        """Удалить книгу."""
        book = self._get_book_by_id(book_id)
        if book:
            self.db.delete_data_by_id(book_id)

        return book

    def search_books(self, field: str | int, value: str | int) -> list[Book]:
        """Поиск книг по переданному параметру."""
        return [Book(**book_data) for book_data in self.db.find_by(field, value)]

    def change_status(self, book_id: str, status: str) -> Book | None:
        """Изменить статус книги по ID."""
        if status not in Book.ALLOW_STATUSES:
            return

        book = self._get_book_by_id(book_id)
        if book:
            book.status = status
            self.db.update_data(book.__dict__)

        return book
