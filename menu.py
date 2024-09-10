#Student id = F221611
from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter.messagebox import showinfo

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from myBookFuncs.bookSearch import *
from myBookFuncs.bookCheckout import *
from myBookFuncs.bookReturn import *
from myBookFuncs.bookSelect import *


def book_selected(book_tree):
    for selected_item in book_tree.selection():
        item = book_tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))


def clear_all(book_tree):
    for book in book_tree.get_children():
        book_tree.delete(book)


def display_books(name_of_book, book_tree):  # adds book record ot book_tree Listbox so it can be displayed
    books = search_book(name_of_book)  # calls function which returns results from what the user searched

    clear_all(book_tree)

    for book in books:
        book_tree.insert("", tk.END, values=book)
    # adds book records to book tree

    book_tree.bind("<<TreeviewSelect>>", book_selected(book_tree))

    # puts eac


def reset_checkout_message(type_of_reset,
                           checkout_status):  # gets rid of the reserve button as it should only appear in some cases
    if type_of_reset == "reserve":
        checkout_status.configure(text="Book Reserved")  # lets user know the book has been reserved
        checkout_process.reserveButton.destroy()  # gets rid of button


def checkout_process(id_member, id_book, checkout_status):  # processes checking out a book
    status = checkout_book(id_member, id_book)  # returns status depending on if the checkout is successful
    if status == "done":
        checkout_status.configure(text="Book Bought")
    elif status == "can reserve":
        checkout_status.configure(text="Unavailable, you can reserve")
        checkout_process.reserveButton = Button(checkout_book_frame, text="Reserve",
                                                command=lambda: [reserve_book(id_member, id_book),
                                                                 reset_checkout_message("reserve", checkout_status)],
                                                width=26)

        checkout_process.reserveButton.grid(column=1, row=3)
        # displays reserve button for if book can be reserved
    elif status == "reservation done":
        checkout_status.configure(text="Book Reserved")
    elif status == "invalid id":
        checkout_status.configure(text="Invalid member id, 4-digit number please")

    else:
        checkout_status.configure(text="Unavailable and can't be reserved")

    # message is displayed depending on the returned status


def return_process(id_book, return_status):  # processes returning a book
    status = return_book(id_book)  # returns status depending on if the return is successful
    if status == "done":
        return_status.configure(text="Book Returned")
    elif status == "book available":
        return_status.configure(text="Book Available")
    elif status == "invalid id":
        return_status.configure(text="Invalid ID")
    # displays message according to status returned


def select_process(budget, select_status):  # processes recommendations based off the budget
    try:
        select_status.configure(text="Selected")  # change status box to show the data has been selected
        float(budget)

        fig, budget_distribution = select_genre(budget)
        canvas = FigureCanvasTkAgg(fig, select_book_frame)
        canvas.draw()
        # puts graph in a form where in can be used a tkinter widget

        average_price_of_books = book_copy_amount()

        recommended_budget_distribution = Listbox(select_book_frame, width=40)
        recommended_budget_distribution.insert(0, "Recommended distribution for your budget")
        recommended_budget_distribution.delete(1, END)

        recommended_book_copies = Listbox(select_book_frame, width=40)
        recommended_book_copies.insert(0, "Recommended book amount per genre")
        recommended_book_copies.delete(1, END)

        # prepares the Listboxes for the data on how it is recommended that the budget should be spent

        i = 1
        for key in budget_distribution:
            recommended_budget_distribution.insert(i, key + " : £" + str(budget_distribution[key]))
            recommended_book_copies.insert(i, key + ": " + str(
                round(budget_distribution[key] / average_price_of_books[i - 1])) + " copies")
            i += 1
        # adds the data to the Listboxes

        recommended_budget_distribution.grid(column=4, row=2, columnspan=1, rowspan=2)
        recommended_book_copies.grid(column=4, row=4, columnspan=1, rowspan=1)
        canvas.get_tk_widget().grid(column=0, row=4, columnspan=4, rowspan=3)
        # adds the widgets to the tab
    except:
        select_status.configure(text="Input Number Please")
    # exception makes sure user has inputted a number for the value to avoid an error


def search_book_setup():  # function to set up search book frame
    search_book_frame.pack(fill='both', expand=True, )
    notebook.add(search_book_frame, text='Search Book')

    columns = ("book_id", "genre", "book_name", "author", "price", "date_bought", "availability")

    book_tree = ttk.Treeview(search_book_frame, columns=columns, show="headings")

    book_tree.heading('book_id', text='Book ID')
    book_tree.heading('genre', text='Genre')
    book_tree.heading('book_name', text='Book Name')
    book_tree.heading('author', text='Author')
    book_tree.heading('price', text='Price')
    book_tree.heading('date_bought', text='Date Bought')
    book_tree.heading('availability', text='Availability')

    # creates headings for the tree

    scrollbar = ttk.Scrollbar(search_book_frame, orient=tk.VERTICAL, command=book_tree.yview)
    book_tree.configure(yscroll=scrollbar.set)

    # adds the search book frame to the notebook

    # creates the tree which displays data from book_info file along with the availability of each of the books

    Label(search_book_frame, text="Book Name:").grid(column=0, row=8)
    book_name = Entry(search_book_frame, width=30)
    search_book_button = Button(search_book_frame, text="Search Book",
                                command=lambda: display_books(book_name.get(), book_tree), width=20, bg="white")

    # creates input for the book name of what the user wil want to search up
    # button is also created to confirm

    book_name.grid(column=1, row=8)
    book_tree.grid(column=0, row=0, columnspan=10, rowspan=5, sticky="nsew")
    scrollbar.grid(column=11, row=0, rowspan=5, sticky="ns")
    search_book_button.grid(column=1, row=9)
    # adds the widgets to the tab


def checkout_book_setup():  # function to set up checkout book frame
    checkout_book_frame.pack(fill='both', expand=True)
    notebook.add(checkout_book_frame, text='Checkout Book')

    # adds the checkout book frame to the notebook

    Label(checkout_book_frame, text="Book Id:").grid(column=0, row=1)
    Label(checkout_book_frame, text="Member ID:").grid(column=0, row=2)
    book_id = Entry(checkout_book_frame, width=30)
    member_id = Entry(checkout_book_frame, width=30)
    checkout_status = Label(checkout_book_frame, text="No Checkout", width=30, bg="white")
    checkout_button = Button(checkout_book_frame, text="Checkout Book",
                             command=lambda: checkout_process(member_id.get(), book_id.get(), checkout_status),
                             width=26)
    # creates input for the book and member id for when the user will checkout a book
    # a status box is also created so that the user is updated on what is happening during the checkout process
    # button is also created to confirm checkout

    book_id.grid(column=1, row=1)
    member_id.grid(column=1, row=2)
    checkout_status.grid(column=2, row=2)
    checkout_button.grid(column=1, row=4)
    # adds the widgets to the tab


def return_book_setup():  # function to set up return book frame
    return_book_frame.pack(fill='both', expand=True)
    notebook.add(return_book_frame, text='Return Book')

    # adds the return book frame to the notebook

    Label(return_book_frame, text="Book Id:").grid(column=0, row=0)
    book_id = Entry(return_book_frame, width=30)
    return_status = Label(return_book_frame, text="No Return", width=30, bg="white")
    return_book_button = Button(return_book_frame, text="Return Book",
                                command=lambda: return_process(book_id.get(), return_status),
                                width=26)
    # creates input for the book id for when the user will return a book
    # a status box is also created so that the user is updated on what is happening during the return process
    # button is also created to confirm return

    book_id.grid(column=1, row=0)
    return_book_button.grid(column=1, row=1)
    return_status.grid(column=2, row=0)
    # adds the widgets to the tab


def select_book_setup():  # function to set up select book frame
    select_book_frame.pack(fill='both', expand=True)
    notebook.add(select_book_frame, text='Select Book')

    # adds the select book frame to the notebook

    best_books = generate_book_rankings()
    best_genres = generate_genre_rankings()
    # gets the best books and genres

    budget_label = Label(select_book_frame, text="Budget:", width=10)
    budget = Entry(select_book_frame, width=30)
    select_status = Label(select_book_frame, text="Nothing selected", bg="white")
    recommended_books_for_purchase_button = Button(select_book_frame, text="Recommend Books to Purchase",
                                                   command=lambda: select_process(budget.get(), select_status),
                                                   width=26)

    # creates input for the budget for when the user will get recommendations
    # a status box is also created so that the user is updated on what is happening during the selection process
    # button is also created to confirm when to calculate the recommendations

    book_ranking = Listbox(select_book_frame, width=54)
    book_ranking.insert(0, "Here are the top books")
    book_ranking.delete(1, END)

    i = 1
    for book in best_books:
        book_ranking.insert(i, str(i) + "." + book[0])
        i += 1

    genre_ranking = Listbox(select_book_frame, width=54)
    genre_ranking.insert(0, "Here are the top genres:")
    genre_ranking.delete(1, END)

    j = 1
    for genre in best_genres:
        genre_ranking.insert(j, str(j) + "." + genre[0])
        j += 1
    genre_ranking.insert(END,
                         f"I recommend buying more {best_genres[0][0]}, {best_genres[1][0]},"
                         f" and {best_genres[2][0]}")

    # Listboxes are created and are inserted with data in order of the most popular in each case

    budget_label.grid(column=0, row=0)
    budget.grid(column=1, row=0)
    select_status.grid(column=2, row=0)
    recommended_books_for_purchase_button.grid(column=1, row=1)

    genre_ranking.grid(column=0, row=2, columnspan=2, rowspan=2)
    book_ranking.grid(column=2, row=2, columnspan=2, rowspan=2)

    # adds the widgets to the tab


win = Tk()
win.title("Library Management System")
win.geometry("1450x700")
win.configure(bg="grey")
# creates tkinter window

notebook = ttk.Notebook(win)
notebook.pack(expand=1, fill="both")
# creates notebook to allow different frames

search_book_frame = ttk.Frame(notebook, width=800, height=560)
checkout_book_frame = ttk.Frame(notebook, width=800, height=560)
return_book_frame = ttk.Frame(notebook, width=800, height=560)
select_book_frame = ttk.Frame(notebook, width=800, height=560)
# create different frames

search_book_setup()
checkout_book_setup()
return_book_setup()
select_book_setup()
# call functions that will set up the frames

win.mainloop()

# execute tkinter event loop
