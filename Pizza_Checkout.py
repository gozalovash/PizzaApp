import sqlite3
import tkinter
from Order_Pizza import *
from Pizza import *
import datetime

class CheckoutPage:
    def __init__(self, master, user_id, conn):
        self.root = master
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.root.grid()
        self.user_id = user_id
        self.cursor.execute("""SELECT username FROM users WHERE id=?""", (user_id, ))
        self.username = str(self.cursor.fetchone())
        self.index = PhotoImage(file="Photos/index_gif.gif")
        self.index = self.index.subsample(20, 20)
        self.label = Label(image=self.index)
        self.label.grid(row=0, column=0, sticky=NW)

        self.b_label = Label(text="Checkout")
        self.b_label.grid(row=0, column=1, columnspan=3, sticky=S)

        self.cursor.execute("""SELECT name, receipt, price FROM card WHERE user_id=?""", (user_id, ))
        self.orders = self.cursor.fetchall()
        self.rows = len(self.orders)
        self.columns = 3
        for i in range(self.rows):
            for j in range(self.columns):
                self.cell = Label(text=str(self.orders[i][j]))
                self.cell.grid(row=i+1, column=j, sticky=SW, padx=4, pady=4)
        self.sum = sum(self.orders[i][2] for i in range(self.rows))
        self.sum_cell = Label(text="Total sum: "+str(self.sum))
        self.sum_cell.grid(row=self.rows+1, column=2, columnspan=2, sticky=SW, padx=4, pady=4)

        self.order = Button(text="Send Order", command=self.order)
        self.order.grid(row=self.rows+2, column=self.columns+1, sticky=SW, padx=4, pady=4)

    def order(self):
        self.message = Label(text="Order Sent! Your Pizza will be delivered as soon as the quarantine is over :-)",
                             width=70)
        self.message.grid(row=self.rows+3, column=0, columnspan=3, sticky=SW, padx=4, pady=4)
        try:
            for i in range(self.rows):
                self.cursor.execute("""INSERT INTO history VALUES (?,?,?,?,?)""",
                            (self.username, self.orders[i][0], self.orders[i][1], self.sum, datetime.datetime.now(), ))
                self.conn.commit()
        except Error:
            pass


def checkout(user_id):
    conn = sqlite3.connect('pizza.db')
    root = Tk()
    root.title("Messy Pizza App")
    root.geometry("800x500+150+30")
    root.configure(bg="#ffcc99")
    my_gui = CheckoutPage(root, user_id, conn)
    root.mainloop()