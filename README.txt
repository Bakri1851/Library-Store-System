Library Management System

In this program I have fulfilled all the criteria

menu.py
I used tkinter to create a GUI for the user to allow them an easy way to use the Library Management System
I have also displayed a matplotlib graph on tkinter
Have also used notebook to allow for each section to be separated to allow a more user-friendly interface
I have used treeview to display my data rather than a listbox as I believe it will give more ease of access to the data
All functions related to GUI is in here

bookSearch.py
Has a function which allows the book search to happen
In the function a list is created based on what the user had searched that is then returned to main to put in the tree

bookCheckout.py
Has functions which allows the book checkout to happen
the checkout_book function checks if the user inputted data is valid to be submitted
-if the data is valid it calls a function from the database to input the data
-if the data is invalid the right message is sent to the user
if the book is unavailable and the user wants to reserve the book the reserve_book function allows for the reservation to take place
-performs suitable checks to see if data is valid to be inputted
-calls a function from the database to input the data if it is valid

bookReturn.py
Has a function which allows the book return to happen
The function performs suitable checks on the book to see if it is valid to be put into the logfile
-If the book is valid to be returned then it calls a function from the database to put this data into the logfile
-if the book isn't valid to be returned and appropriate message is returned to notify the user of this

bookSelect.py
Contains functions which show the top books and genres as well as calculate a recommendation on how to distribute the user inputted budget
top_results orders the list in order of most popular to least popular
create_graph generates a graph for how popular each genre is
book_copy_amount calculates the average price of a book from each genre
generate_book_rankings and generate_genre_rankings genre creates dictionaries for the books and genres respectively which returns an ordered dictionary of most popular book/genres to least popular
select_genre calculates how to distribute the user inputted budget

database.py
contains common functions which are used in other files of the program
read_files takes the Book_Info.txt and logfile.txt and returns the files in a list form, so it can be worked with
add_record appends new logs to the log files. The type of log depends on the log type requested

Book_Info.txt
Contains all the book copies and the details of each book

logfile.txt
Contains all the logs in order of date so that the data can be managed correctly. Each log consists of when a book was borrowed