import requests
from typing import List
from modules.book.book import Book

class BookServices():
    
    @staticmethod
    def search_books(query: str) -> List[Book]:
        response = requests.get(f"https://learning.oreilly.com/api/v2/search/?query={query}")

        books : List[Book] = []

        for result in response.json()["results"]:
            book = Book()
            book.id = result["archive_id"]
            book.title = result["title"]
            book.description = result.get("description")
            book.link = result["url"]

            books.append(book)

        return books