from typing import Optional
from modules.book.book import Book
from modules.detailed_book.detailed_book_services import DetailedBook
from modules.book.book_services import BookServices

class DetailedBookServices(Book):

    @staticmethod
    def get_detailed_book(book: str) -> Optional[DetailedBook]:
        books = BookServices.search_books(book)

        if not books:
            return None

        detailed_book = DetailedBook(books[0])
        return detailed_book
