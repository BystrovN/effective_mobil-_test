import os
import unittest
from unittest.mock import MagicMock

from database import Database
from objects.library import Library
from objects.book import Book


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_library_data.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.db = Database(self.test_file)
        self.book_data = {'title': 'Book1', 'author': 'Author1', 'year': 2021, 'id': '1'}

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_data_empty(self):
        self.assertEqual(self.db.data, [])

    def test_append_data(self):
        self.db.append_data(self.book_data)
        self.assertEqual(len(self.db.data), 1)

    def test_find_by(self):
        self.db.append_data(self.book_data)
        result = self.db.find_by('title', 'Book1')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Book1')

    def test_delete_data_by_id(self):
        self.db.append_data(self.book_data)
        self.db.delete_data_by_id(self.book_data['id'])
        self.assertEqual(len(self.db.data), 0)

    def test_update_data(self):
        self.db.append_data(self.book_data)
        updated_data = self.book_data.copy()
        updated_data['title'] = 'Updated Book'
        self.db.update_data(updated_data)
        updated = self.db.find_by('title', 'Updated Book')
        self.assertEqual(len(updated), 1)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(Database)
        self.library = Library(self.db)
        self.book_data = {'title': 'Title', 'author': 'Author', 'year': 2021, 'id': '1', 'status': 'в наличии'}
        self.book = Book(**self.book_data)

    def test_add_book(self):
        self.db.append_data = MagicMock()
        book = self.library.add_book('Title', 'Author', 2021)
        self.db.append_data.assert_called_once_with(book.__dict__)
        self.assertEqual(book.title, 'Title')
        self.assertEqual(book.status, 'в наличии')

    def test_delete_book(self):
        self.db.find_by = MagicMock(return_value=[self.book_data])
        self.db.delete_data_by_id = MagicMock()
        book = self.library.delete_book('1')
        self.db.delete_data_by_id.assert_called_once_with('1')
        self.assertEqual(book.title, 'Title')

    def test_search_books(self):
        self.db.find_by = MagicMock(return_value=[self.book_data])
        books = self.library.search_books('title', 'Title')
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, 'Title')

    def test_fail_search_books(self):
        self.db.find_by = MagicMock(return_value=[])
        books = self.library.search_books('title', 'Title')
        self.assertEqual(len(books), 0)

    def test_change_status(self):
        self.db.find_by = MagicMock(return_value=[self.book_data])
        self.db.update_data = MagicMock()
        book = self.library.change_status('1', 'выдана')
        self.db.update_data.assert_called_once_with(book.__dict__)
        self.assertEqual(book.status, 'выдана')

    def test_change_status_invalid(self):
        self.db.find_by = MagicMock(return_value=[self.book_data])
        self.db.update_data = MagicMock()
        book = self.library.change_status('1', 'invalid_status')
        self.db.update_data.assert_not_called()
        self.assertIsNone(book)


if __name__ == '__main__':
    unittest.main()
