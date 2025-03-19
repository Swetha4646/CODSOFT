import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3



def create_table():
    with sqlite3.connect("Users.db") as db:
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            Username TEXT NOT NULL, 
            GeneratePassword TEXT NOT NULL
        );
        """)
        db.commit()


class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.Passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()

        master.title('Password Generator')
        master.geometry('660x500')
        master.config(bg='#FF8000')
        master.resizable(False, False)

        self.label = Label(text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        self.user = Label(text="Enter user Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.user.grid(row=1, column=0)

        self.textfield = Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=1, column=1)
        self.textfield.focus_set()

        self.length = Label(text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.length.grid(row=2, column=0)

        self.password_length_entry = Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.password_length_entry.grid(row=2, column=1)

        self.generated_password = Label(text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.generated_password.grid(row=3, column=0)

        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge')
        self.generated_password_textfield.grid(row=3, column=1)

        self.generate = Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1,
                               font=('Verdana', 15, 'bold'), fg='#458B00', command=self.generate_pass)
        self.generate.grid(row=4, column=1)

        self.accept = Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1,
                             font='Helvetica 15 bold italic', fg='#458B00', command=self.accept_fields)
        self.accept.grid(row=5, column=1)

        self.reset = Button(text="RESET", bd=3, relief='solid', padx=1, pady=1,
                            font='Helvetica 15 bold italic', fg='#458B00', command=self.reset_fields)
        self.reset.grid(row=6, column=1)

    def generate_pass(self):
        """ Generate a secure random password """
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%()\"?!"
        numbers = "1234567890"
        name = self.textfield.get()
        leng = self.n_passwordlen.get()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if not name.isalpha():
            messagebox.showerror("Error", "Name must contain only letters")
            return

        if leng < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        password = (
            random.sample(upper, random.randint(1, leng - 3)) +
            random.sample(lower, random.randint(1, leng - 3)) +
            random.sample(chars, random.randint(1, leng - 3)) +
            random.sample(numbers, leng - 3)
        )

        random.shuffle(password)
        gen_password = "".join(password)
        self.generated_password_textfield.delete(0, END)
        self.generated_password_textfield.insert(0, gen_password)

    def accept_fields(self):
        """ Store the username and password in the database """
        name = self.n_username.get()
        password = self.n_generatedpassword.get()

        if not name or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty!")
            return

        try:
            with sqlite3.connect("Users.db", timeout=5) as db:
                cursor = db.cursor()

                
                cursor.execute("SELECT * FROM users WHERE Username = ?", (name,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "This username already exists!")
                else:
                    cursor.execute("INSERT INTO users (Username, GeneratePassword) VALUES (?, ?)", (name, password))
                    db.commit()
                    messagebox.showinfo("Success", "Password saved successfully!")

        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Failed due to {str(e)}")

    def reset_fields(self):
        """ Reset all input fields """
        self.textfield.delete(0, END)
        self.n_passwordlen.set(0)
        self.generated_password_textfield.delete(0, END)


if __name__ == '__main__':
    create_table()
    root = Tk()
    app = GUI(root)
    root.mainloop()
