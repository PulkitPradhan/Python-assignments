import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from library_manager.inventory import LibraryInventory

logging.basicConfig(filename='library.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    inventory = LibraryInventory()
    
    while True:
        print("\n=== Library Inventory Manager ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        try:
            if choice == '1':
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                isbn = input("Enter ISBN: ")
                if title and author and isbn:
                    inventory.add_book(title, author, isbn)
                    logging.info(f"Added book: {title}")
                else:
                    print("Error: All fields are required!")

            elif choice == '2':
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book:
                    if book.issue():
                        inventory.save_books()
                        print(f"Book '{book.title}' issued successfully.")
                        logging.info(f"Issued book: {book.title}")
                    else:
                        print("Error: Book is already issued.")
                else:
                    print("Error: Book not found.")

            elif choice == '3':
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book:
                    if book.return_book():
                        inventory.save_books()
                        print(f"Book '{book.title}' returned successfully.")
                        logging.info(f"Returned book: {book.title}")
                    else:
                        print("Error: Book was not issued.")
                else:
                    print("Error: Book not found.")

            elif choice == '4':
                inventory.display_all()

            elif choice == '5':
                query = input("Enter Title to search: ")
                results = inventory.search_by_title(query)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("No books found.")

            elif choice == '6':
                print("Exiting... Goodbye!")
                break

            else:
                print("Invalid choice! Please try again.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
