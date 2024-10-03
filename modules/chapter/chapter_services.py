from typing import List

import requests
from modules.book.book import Book
from modules.chapter.chapter import Chapter

class ChapterService:

    @staticmethod
    def get_all_chapters(book: Book) -> List[Chapter]:
        book_data = requests.get(book.link).json()

        if not book_data.get("chapter_list"):
            return []
        
        chapter_data = requests.get(book_data["chapter_list"]).json()

        chapters : List[Chapter] = []

        for chapter in chapter_data["results"]:
            chapter_object = Chapter()
            chapter_object.title = chapter["title"]

            chapters.append(chapter_object)

        return chapters