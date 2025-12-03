import json
import os
from library_manager.book import Book

class LibraryInventory:
    def __init__(self, filename="library_data.json"):
        self.books = []
        self.filename = filename
        self.load_books()

    def add_book(self, title, author, isbn):
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_books()
        print(f"Book '{title}' added successfully.")

    def search_by_title(self, title):
        results = []
        for book in self.books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        else:
            for book in self.books:
                print(book)

    def save_books(self):
        try:
            data = [book.to_dict() for book in self.books]
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_books(self):
        if not os.path.exists(self.filename):
            return  # File doesn't exist yet, start with empty list

        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.books = []
                for item in data:
                    # Recreate Book objects from dictionary data
                    book = Book(item['title'], item['author'], item['isbn'], item['status'])
                    self.books.append(book)
        except (json.JSONDecodeError, IOError):
            print("Error loading data. Starting with empty inventory.")
            self.books = []