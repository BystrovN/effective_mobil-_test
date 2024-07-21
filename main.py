import sys

import config
from database import Database
from objects.library import Library


def set_db():
    """Инициализация БД."""
    return Database(config.DATABASE)


class Main:
    """Класс для управления пользовательским интерфейсом приложения библиотеки книг."""

    INVALID_VALUE = 'Некорректное значение'

    def __init__(self, db: Database):
        self.library = Library(db)
        self.actions = {
            '1': self._add_book,
            '2': self._delete_book,
            '3': self._search_book,
            '4': self._display_all_books,
            '5': self._change_book_status,
            '6': self._exit_program,
        }

    def _is_int(self, value: str) -> bool:
        """Является ли значение числом."""
        return value.isdigit()

    def _is_filled(self, value: str) -> bool:
        """Заполнено ли значение."""
        return bool(value)

    def _input_with_validation(self, msg: str, validation_func) -> str:
        """Получение и валидация данных от пользователя."""
        value = input(msg)
        if not validation_func(value):
            print(self.INVALID_VALUE)
            return self._input_with_validation(msg, validation_func)

        return value

    def _print_menu(self) -> None:
        print('Выберите действие:')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Искать книгу')
        print('4. Отобразить все книги')
        print('5. Изменить статус книги')
        print('6. Выйти')
        print('\n')

    def _get_book_data(self) -> tuple[str, str, int]:
        title = self._input_with_validation('Введите название книги: ', self._is_filled)
        author = self._input_with_validation('Введите автора книги: ', self._is_filled)
        year = int(self._input_with_validation('Введите год издания книги: ', self._is_int))
        return title, author, year

    def _add_book(self) -> None:
        title, author, year = self._get_book_data()
        book = self.library.add_book(title, author, year)
        print(f'Книга добавлена: {book}')

    def _delete_book(self) -> None:
        book_id = input('Введите ID книги для удаления: ')
        book = self.library.delete_book(book_id)
        if book:
            print(f'Книга удалена: {book}')
        else:
            print('Книга не найдена')

    def _search_book(self) -> None:
        field = input('Искать по (title/author/year): ')
        value = input(f'Введите значение для поиска по {field}: ')
        books = self.library.search_books(field, value)
        if not books:
            print('Книги не найдены')
            return

        for book in books:
            print(book)

    def _display_all_books(self) -> None:
        books = self.library.get_all_books()
        print(f'Всего книг - {len(books)}')
        for book in books:
            print(book, '\n')

    def _change_book_status(self) -> None:
        book_id = input('Введите ID книги для изменения статуса: ')
        status = input("Введите новый статус ('в наличии' или 'выдана'): ")
        book = self.library.change_status(book_id, status)
        if book:
            print(f'Статус книги изменен: {book}')
        else:
            print('Книга не найдена или статус некорректный')

    def _exit_program(self) -> None:
        print('\nВыход из программы')
        sys.exit()

    def run(self) -> None:
        """Главный метод работы с терминалом."""
        try:
            self._print_menu()
            choice = input('Введите номер действия: ')
            action = self.actions.get(choice)
            if action:
                print('\n')
                action()
                print('\n')
            else:
                print(self.INVALID_VALUE, '\n')

            return self.run()

        except KeyboardInterrupt:
            self._exit_program()


if __name__ == '__main__':
    db = set_db()
    Main(db).run()
