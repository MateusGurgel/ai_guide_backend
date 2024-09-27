from typing import List
from modules.book.book import Book
from modules.chapter.chapter import Chapter
from modules.chapter.chapter_services import ChapterService


class DetailedBook(Book):
  title: str
  description: str
  chapters: List[Chapter]

  def __init__(self, book: Book) -> None:
    self.id = book.id
    self.title = book.title
    self.description = book.description
    self.link = book.link

    self.chapters : List[Chapter] = ChapterService().get_all_chapters(book)

  def __str__(self) -> str:
    title_description = f"{self.title} - {self.description}"
    chapters = "\n".join([str(chapter) for chapter in self.chapters])
    return f"{title_description}\n\nChapters:\n{chapters}"