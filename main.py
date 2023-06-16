import tkinter as tk
import mysql.connector
from screeninfo import get_monitors
from tkinter import ttk

root = tk.Tk()
import tkinter as tk
import mysql.connector
from screeninfo import get_monitors
from tkinter import ttk

# ...

def create_table():
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="krawik",
        database="studentsdb"
    )
    mycursor = mydb.cursor()

    # Sprawdzenie istnienia tabeli
    table_exists = False
    mycursor.execute("SHOW TABLES LIKE 'student'")
    result = mycursor.fetchone()
    if result:
        table_exists = True

    # Tworzenie tabeli tylko wtedy, gdy nie istnieje
    if not table_exists:
        sql = """
            CREATE TABLE `student` (
              `id` int NOT NULL AUTO_INCREMENT,
              `name` varchar(45) DEFAULT NULL,
              `surname` varchar(45) DEFAULT NULL,
              `year` varchar(45) DEFAULT NULL,
              `major` varchar(45) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        mycursor.execute(sql)
        mydb.commit()
        print("Table 'student' created successfully.")
    else:
        print("Table 'student' already exists.")

    mycursor.close()
    mydb.close()

# ...
def insert_student(name, surname, year, major):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="krawik",
        database="studentsdb"
    )
    mycursor = mydb.cursor()
    insert_query = """
    INSERT INTO student (name, surname, year, major)
    VALUES (%s, %s, %s, %s)
    """
    students_data = [
        (name, surname, year, major),
    ]
    for student in students_data:
        mycursor.execute(insert_query, student)

    result = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    mydb.close()
    return result
# Call create_table() function before inserting data
create_table()

insert_student("John", "Doe", "2023", "Computer Science")
insert_student("Jane", "Smith", "2022", "Psychology")
insert_student("Michael", "Johnson", "2024", "Business Administration")
insert_student("Emily", "Williams", "2023", "Art History")
insert_student("David", "Brown", "2022", "Engineering")

# ...


def load_data():
    data = fetch_data()
    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=row)


root.title("Students tool")
screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height
root.geometry(f"{int(screen_width / 1.5)}x{int(screen_height / 1.5)}")

left_frame = tk.Frame(root, borderwidth=4, relief="ridge", width=int(screen_width / 8), height=int(screen_width / 4))
left_frame.pack(side="left", padx=10, pady=10)
left_frame.pack_propagate(0)

nameLabel = tk.Label(left_frame, text="Podaj imię")
nameEntry = tk.Entry(left_frame)
nameLabel.pack(anchor="center", padx=10, pady=10)
nameEntry.pack(anchor="center", padx=10, pady=10)

surnameLabel = tk.Label(left_frame, text="Podaj nazwisko")
surnameEntry = tk.Entry(left_frame)
surnameLabel.pack(anchor="center", padx=10, pady=10)
surnameEntry.pack(anchor="center", padx=10, pady=10)

yearLabel = tk.Label(left_frame, text="Rok studiów")
yearEntry = tk.Scale(left_frame, from_=1, to=5, orient=tk.HORIZONTAL)
yearLabel.pack(anchor="center", padx=10, pady=10)
yearEntry.pack(anchor="center", padx=10, pady=10)

values = ["informatyka", "grafika", "zarzadzanie", "architektura"]

majorLabel = tk.Label(left_frame, text="Podaj kierunek studiów")
majorCombobox = ttk.Combobox(left_frame, values=values)
majorCombobox.state(["readonly"])
majorLabel.pack(anchor="center", padx=10, pady=10)
majorCombobox.pack(anchor="center", padx=10, pady=10)
resultLabel = tk.Label(root, text="")
resultLabel.pack()


def change_text():
    name = nameEntry.get()
    resultLabel.config(text=name + " has been added.")


def add_student():
    name = str(nameEntry.get())
    surname = str(surnameEntry.get())
    year = str(yearEntry.get())
    major = str(majorCombobox.get())
    insert_student(name, surname, year, major)
    load_data()
    resultLabel.config(text=f"{name} has been added.")











def fetch_data():
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="krawik",
        database="studentsdb"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM student")
    result = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return result



addButton = tk.Button(left_frame, text="Add Student", command=add_student)
addButton.pack(anchor="center", padx=10, pady=10)

treeview = ttk.Treeview(root)
treeview["columns"] = ("ID", "Name", "Surname", "Year", "Major")
treeview.column("#0", width=0)
treeview.heading("ID", text="ID")
treeview.heading("Name", text="Imie")
treeview.heading("Surname", text="Nazwisko")
treeview.heading("Year", text="Rok Studiow")
treeview.heading("Major", text="Kierunek")
treeview.pack()





load_data()


def open_details_window(event):
    # Pobranie zaznaczonego elementu
    selected_item = treeview.focus()
    if selected_item:
        # Pobranie danych z zaznaczonego elementu
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]

        # Tworzenie nowego okna
        details_window = tk.Toplevel(root)
        details_window.title("Szczegóły")

        # Tworzenie i wyświetlanie widgetów opartych na danych z zaznaczonego elementu

        id_label = ttk.Label(details_window, text="Id")
        id_label.pack()
        id_entry = ttk.Entry(details_window)
        id_entry.insert(0, item_values[0])
        id_entry.config(state="disabled")
        id_entry.pack()

        name_label = ttk.Label(details_window, text="Imie")
        name_label.pack()
        name_entry = ttk.Entry(details_window)
        name_entry.insert(0, item_values[1])
        name_entry.pack()

        surname_label = ttk.Label(details_window, text="Nazwisko")
        surname_label.pack()
        surname_entry = ttk.Entry(details_window)
        surname_entry.insert(0, item_values[2])
        surname_entry.pack()

        year_label = ttk.Label(details_window, text="Rok:")
        year_label.pack()
        year_entry = ttk.Entry(details_window)
        year_entry.insert(0, item_values[3])
        year_entry.pack()

        major_label = ttk.Label(details_window, text="Kierunek:")
        major_label.pack()
        major_entry = ttk.Entry(details_window)
        major_entry.insert(0, item_values[4])
        major_entry.pack()

        print(item_values[0])
        delete_button = tk.Button(details_window, text="Usuń", command=lambda: delete_student(item_values[0]))
        delete_button.pack()

        update_button = tk.Button(details_window, text="Edytuj",
                                  command=lambda: update_data(item_values[0], name_entry.get(), surname_entry.get(),
                                                              year_entry.get(), major_entry.get()))
        update_button.pack()


treeview.bind("<Double-1>", open_details_window)


def update_data(id, name, surname, year, major):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="krawik",
        database="studentsdb"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE student SET name = %s, surname = %s, year = %s, major = %s WHERE id = %s"
    params = (name, surname, year, major, id)
    mycursor.execute(sql, params)
    mydb.commit()
    mycursor.close()
    mydb.close()
    load_data()
    resultLabel.config(text="Data updated successfully.")


def delete_student(id):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="krawik",
        database="studentsdb"
    )
    mycursor = mydb.cursor()
    sql = "DELETE FROM student WHERE ID = %s"
    params = (id,)
    mycursor.execute(sql, params)
    mydb.commit()
    mycursor.close()
    mydb.close()
    load_data()
    resultLabel.config(text="Student has been deleted.")


root.mainloop()
