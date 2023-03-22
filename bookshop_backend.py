# ======PROGRAMME DETAILS======
# This programme creates a database and fills it with five books, including a primary key for ID, a title, author
# and quantity count.
# Four functions are defined, allowing us to add, update, delete, and search for books in the table stored on the db.
# Finally, an interactive menu is given allowing a user to call each of the functions.

import sqlite3
db = sqlite3.connect("bookshop")
cursor = db.cursor()

cursor.execute("CREATE TABLE bookshop_stock (id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)")

stock_info = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
              (3002, "Harry Potter and The Philosopher's Stone", "J.K. Rowling", 40),
              (3003, "The Lion, The Witch, and The Wardrobe", "C.S. Lewis", 25),
              (3004, "The Lord of The Rings", "J.R.R. Tolkien", 37),
              (3005, "Alice in Wonderland", "Lewis Carroll", 12),
              ]
cursor.executemany('''INSERT INTO bookshop_stock(id, Title, Author, Qty) VALUES(?,?,?,?)''', stock_info)
db.commit()


# This function allows us to add a new book to the table bookshop_stock.
def add():
    # Here we select the largest id from the bookshop stock in order to add 1 to it and give it an automatic value
    # for the primary key. The rest of the information is manually entered.
    new_stock_info = ()
    cursor.execute("SELECT MAX(id) FROM bookshop_stock")
    largest_id = cursor.fetchone()
    id = 1 + largest_id[0]
    new_stock_info = new_stock_info + (id, )
    title = input("Enter the title of the book:\n")
    author = input("Enter the author of the book:\n")
    qty = int(input("Enter the number of copies in stock:\n"))
    db.commit()

    # Here we set up one condition, controlling for the datatype entered into the database. It would be terrible to
    # mess up datatypes and make our database unusable. If the types are correct, then the new book is entered into the
    # system.
    if type(title) == str:
        new_stock_info = new_stock_info + (title, )
        if type(author) == str:
            new_stock_info = new_stock_info + (author, )
            if type(qty) == int:
                new_stock_info = new_stock_info + (qty, )
                print(new_stock_info)
                cursor.execute("INSERT INTO bookshop_stock (id, Title, Author, Qty) VALUES (?,?,?,?)", new_stock_info)
                db.commit()
                print("You have entered a new book into the system.")
            else:
                print("Sorry, you have entered the wrong datatype into the quantity field. Integers only please.")
        else:
            print("Sorry, you have entered the wrong datatype into the author field. Text only please.")
    else:
        print("Sorry, you have entered the wrong datatype into the title field. Text only please.")


# This function allows us to go into a specific book and update any or all of the columns in the table for that book.
def update():

    # Here we enter the desired book id to update and check that it's actually in the table before proceeding.
    update_id = int(input("Enter the id of the book you want to update the details of:\n"))
    cursor.execute("SELECT id FROM bookshop_stock")
    id_check = [id_key[0] for id_key in cursor.fetchall()]
    db.commit()

    # If the id is in the table, then we proceed to update each of the columns in turn, giving the user the opportunity
    # to skip over a column. Useful if a mistake was made in adding a book, or when a book is sold and only
    # the qty column is needed to be updated.
    if update_id in id_check:
        title_option = input("Would you like to update the title? Enter \'yes\' or \'no\':\n")
        if title_option.lower() == "yes":
            new_title = input("Enter the new title:\n")
            if type(new_title) == str:
                cursor.execute('''UPDATE bookshop_stock SET Title = ? WHERE id = ?''', (new_title, update_id))
                db.commit()
            else:
                print("Sorry, that datatype input wasn't recognised. You will have to restart the process to "
                      "update the title.")
        elif title_option.lower() == "no":
            pass
        else:
            print("Sorry, that input wasn't recognised. You will have to restart this process to update the title.")

        # Here is the author update. It's basically identical to the above block of code.
        author_option = input("Would you like to update the author? Enter \'yes\' or \'no\':\n")
        if author_option.lower() == "yes":
            new_author = input("Enter the new author:\n")
            if type(new_author) == str:
                cursor.execute('''UPDATE bookshop_stock SET Author = ? WHERE id = ?''', (new_author, update_id))
                db.commit()
            else:
                print("Sorry, that datatype input wasn't recognised. You will have to restart the process to "
                      "update the author.")
        elif author_option.lower() == "no":
            pass
        else:
            print("Sorry, that input wasn't recognised. You will have to restart this process to update the author.")

        # And again, the quantity update block of code.
        qty_option = input("Would you like to update the quantity in stock? Enter \'yes\' or \'no\':\n")
        if qty_option.lower() == "yes":
            new_qty = int(input("Enter the new quantity:\n"))
            if type(new_qty) == int:
                cursor.execute('''UPDATE bookshop_stock SET Qty = ? WHERE id = ?''', (new_qty, update_id))
                db.commit()
            else:
                print("Sorry, that datatype input wasn't recognised. You will have to restart the process to "
                      "update the quantity.")
        elif qty_option.lower() == "no":
            pass
        else:
            print("Sorry, that input wasn't recognised. You will have to restart this process to update the quantity.")


    # This else clause is to catch cases of IDs that aren't in the table. We offer the option to print all the books in
    # stock with their IDs, which allows users to see if their desired ID is actually in the table.
    else:
        stock_check = input("That id doesn't appear to be in the database. Would you like to look at the database to "
                            "check the currently available ids? Enter \'yes\' or \'no\':\n")
        while stock_check != "no":
            if stock_check.lower() == "yes":
                print("Here are the available books in storage. Please make sure you only pick an ID from here:\n")
                cursor.execute("SELECT * FROM bookshop_stock")
                for row in cursor.fetchall():
                    print(row)
                db.commit()
                print("\n")
                stock_check = "no"
            else:
                print("Sorry, that input wasn't recognised.")


# This function allows us to delete individual books or the entire table.
def delete():
    delete_options = input("Would you like to delete one book or the entire stock? Enter \'one\' or \'all\'. "
                           "Enter any other key to return to the main menu:\n")

    # In this if-block we enter a unique ID to delete the specific row in the table. Because it is just one book, we
    # include a single failsafe.
    if delete_options.lower() == "one":
        id_delete = int(input("Enter the id of the book you want to delete:\n"))
        cursor.execute("SELECT Title FROM bookshop_stock WHERE id = ?", (id_delete,))
        title_check = cursor.fetchone()
        print(title_check)
        db.commit()

        if title_check is not None:
            failsafe = input(f"Are you sure you want to delete '{title_check[0]}'? Enter 'yes' or 'no':\n")
            if failsafe.lower() == "yes":
                cursor.execute('''DELETE FROM bookshop_stock WHERE id = ?''', (id_delete,))
                db.commit()
            elif failsafe.lower() == "no":
                pass
            else:
                print("Your input wasn't recognised. You will have to restart the process to delete a book.")

    # This elif-block is for deleting all books in the table. Because this is a big risk, we include two failsafes.
    elif delete_options.lower() == "all":
        failsafe_1 = input("You are about to delete all the books you have saved in your database.\n"
                           "Are you absolutely sure you want to do that? Enter \'Yes\' if you are happy with deleting\n"
                           "all the books in your database, or \'No\' if you do not want that.\n")
        if failsafe_1.lower() == "yes":
            failsafe_2 = input("Deleting these books is an irreversible action. Are you certain you want to proceed?\n"
                               "Enter \'Yes\' if you want to proceed with deleting all the books, or \'No\' if you\n"
                               "want to return to the main menu:\n")
            if failsafe_2.lower() == "yes":
                cursor.execute("DELETE FROM bookshop_stock")
                db.commit()
                print("The records of your books have been deleted.")
            elif failsafe_2.lower() == "no":
                print("Returning you to the main menu.")
            else:
                print("That input was not recognised. Returning you to the main menu.")
        elif failsafe_1.lower() == "no":
            pass
        else:
            print("That input was not recognised. "
                  "Out of concern for data safety you are being returned to the main menu.")
    else:
        print("Returning to main menu.")


# This function allows us to search and print every book, an individual book by ID, and all the books with a quantity
# of less than 5 for restock purposes.
def search():

    while True:
        search_choice = input("\nWelcome to the search bar.\n"
                              "Enter \'ev\' to print all the books we have in storage.\n"
                              "Enter \'id\' to print a select book in storage.\n"
                              "Enter \'q\' to print all books with a quantity less than 5 in storage.\n"
                              "And press \'x\' to return to the main menu.\n")

        # This block prints every row/book in the table.
        if search_choice.lower() == "ev":
            cursor.execute("SELECT * FROM bookshop_stock")
            for row in cursor.fetchall():
                print(row)
            db.commit()

        # This block prints individual books based on their ID.
        elif search_choice.lower() == "id":
            id_choice = input("Please enter the id of the book you want to search:\n")
            cursor.execute('''SELECT * FROM bookshop_stock WHERE id = ?''', (id_choice,))
            display_book = cursor.fetchall()
            print(display_book)
            db.commit()

        # This block prints every book with less than 5 copies in stock.
        elif search_choice.lower() == "q":
            cursor.execute("SELECT * FROM bookshop_stock WHERE qty < 5")
            display_books = cursor.fetchall()
            print(display_books)

        # And this breaks the While loop.
        elif search_choice.lower() == "x":
            break

        else:
            print("Input not recognised. Please try again.")


while True:
    menu = input("\nWelcome to the bookshop stock menu. Please choose from any of the following options:\n"
                 "Enter \'a\' to add information to the store's stock.\n"
                 "Enter \'u\' to update information about a book currently in stock.\n"
                 "Enter \'d\' to delete a book from the database.\n"
                 "Enter \'s\' to search for information about books you have in stock.\n"
                 "Enter \'e\' to exit the programme.\n")

    if menu.lower() == "a":
        add()
    elif menu.lower() == "u":
        update()
    elif menu.lower() == "d":
        delete()
    elif menu.lower() == "s":
        search()
    elif menu.lower() == "e":
        print("Ciao!")
        db.close()
        break
    else:
        print("Sorry, that's not a valid input. Please try again.")
