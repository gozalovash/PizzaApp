from tkinter import *
import Order_Pizza
from Pizza import *
import Generate_db
import Admin_page


class LoginPage:
    root = 0

    def __init__(self, master):
        self.root = master
        self.root.grid()
        Generate_db.generate()

        # self.root.title = "Login Page"

        # ============== Database connection ====================

        self.con = sqlite3.connect("pizza.db")
        self.curs = self.con.cursor()

        # ============ Index Image  =============================

        self.index = PhotoImage(file="Photos/index_gif.gif")
        self.index = self.index.subsample(20, 20)
        self.label = Label(image=self.index)
        self.label.grid(row=0, column=0, sticky=NW)

        # ============= Login Field =====================

        self.username = Label(text="Username:")
        self.username.grid(row=1, column=0)
        self.l_username = Entry(width=30)
        self.l_username.grid(row=1, column=1, sticky=S, padx=4, pady=4)

        self.password = Label(text="Password:")
        self.password.grid(row=2, column=0)
        self.l_password = Entry(width=30, show="*")
        self.l_password.grid(row=2, column=1, sticky=S, padx=4, pady=4)

        self.login = Button(text="Login",
                            command=lambda: {self.login_user(self.l_username.get(), self.l_password.get())})
        self.login.grid(row=3, column=0, sticky=S, padx=4, pady=4)
        self.register = Button(text="New to app? Register here ->", bg="#ffcc99",
                               command=lambda: {self.register_user()})
        self.register.grid(row=3, column=1, sticky=S, padx=4, pady=4)

    def login_user(self, l_username, l_password):
        self.curs.execute("SELECT username, password FROM users WHERE username=?", (l_username,))
        self.user = self.curs.fetchone()
        if self.user is not None:
            if l_username == "admin" and self.user[1] == l_password:
                self.root.destroy()
                Admin_page.call_admin()
            elif self.user[1] == l_password:
                print("Logged in successfully!")
                self.root.destroy()
                Order_Pizza.order(l_username)
            else:
                self.message = Message(text='Wrong Password! Try again or Register', width=250)
                self.message.grid(row=4, column=0, columnspan=2, sticky=SE, padx=4, pady=4)
        else:
            self.message = Message(text="No such user! Try again or Register", width=250)
            self.message.grid(row=4, column=0, columnspan=2, sticky=SE, padx=4, pady=4)

    def register_user(self):
        self.top = Toplevel(self.root)
        Registration(self.top)



class Registration:
    def __init__(self, master):
        self.connection = sqlite3.connect('pizza.db')
        self.cursor = self.connection.cursor()
        self.root = master
        self.root.geometry("700x400+300+50")
        self.root.grid()
        self.index = PhotoImage(file="Photos/index_gif.gif")
        self.index = self.index.subsample(20, 20)
        self.label = Label(self.root, image=self.index)
        self.label.grid(row=0, column=0, sticky=NW)
        # ============= Register Field ===================

        self.username = Label(self.root, text="Username:")
        self.username.grid(row=1, column=0)
        self.r_username = Entry(self.root, width=30)
        self.r_username.grid(row=1, column=1, sticky=S, padx=4, pady=4)

        self.password = Label(self.root, text="Password:")
        self.password.grid(row=2, column=0)
        self.r_password = Entry(self.root, width=30, show="*")
        self.r_password.grid(row=2, column=1, sticky=S, padx=4, pady=4)

        self.register = Button(self.root, text="Register user",
                               command=lambda: {self.register_user(self.r_username.get(), self.r_password.get())})
        self.register.grid(row=3, column=0, sticky=S, padx=4, pady=4)

    def register_user(self, username, password):
        self.cursor.execute("""SELECT * FROM users WHERE username=?""", (username,))
        self.existing = self.cursor.fetchone()
        if self.existing is None:
            self.cursor.execute("""INSERT INTO users VALUES (?, ?, ?)""", (None, username, password))
            self.connection.commit()
            self.message = Message(self.root, text="Registered successfully! You are welcome to Login", width=250)
            self.message.grid(row=4, column=0, columnspan=2, sticky=SE, padx=4, pady=4)
        else:
            self.message = Message(self.root, text="User with this name already exists.", width=250)
            self.message.grid(row=4, column=0, columnspan=2, sticky=SE, padx=4, pady=4)

def main():
    root = Tk()
    root.title("Messy Pizza App")
    root.geometry("700x400+150+30")
    root.configure(bg="#ffcc99")
    login = LoginPage(root,)
    root.mainloop()

if __name__ == "__main__":
    main()
