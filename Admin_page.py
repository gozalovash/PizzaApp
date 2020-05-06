import sqlite3
import tkinter
from Order_Pizza import *
from Pizza import *
import datetime

class MyPage:
    def __init__(self, master, conn):
        self.root = master
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.root.grid()
    # ============== HISTORY ==================
        self.cursor.execute("""SELECT * FROM history""")
        self.history = self.cursor.fetchall()
        self.rows = len(self.history)
        self.columns = 5

        if not self.history:
            self.message = Label(text="No history yet!", width=30, bg="#ffcc99")
            self.message.grid(row=0, column=0, padx=10, pady=10)

        for i in range(self.rows):
            for j in range(self.columns):
                self.cell = Label(text=str(self.history[i][j]))
                self.cell.grid(row=i+1, column=j, padx=3, pady=3, sticky=SW)


def call_admin():
    conn = sqlite3.connect('pizza.db')
    root = Tk()
    root.title("Messy Pizza App")
    root.geometry("800x500+150+30")
    root.configure(bg="#ffcc99")
    my_gui = MyPage(root, conn)
    root.mainloop()
