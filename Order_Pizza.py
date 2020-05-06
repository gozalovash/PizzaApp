import Pizza
from tkinter import *
import sqlite3
from sqlite3 import Error
import Pizza_Checkout

pizza_type = Pizza.PizzaBuilder

class PizzaOrder:
    # root1 = 0

    # i = 1

    def __init__(self, master, username, conn):
        self.root1 = master
        self.root1.grid()
        # ============== Database connection ====================
        self.con = sqlite3.connect("pizza.db")
        self.curs = self.con.cursor()
        try:
            self.curs.execute("""CREATE TABLE card(id integer PRIMARY KEY, user_id integer, name text, receipt text, 
            price float)""")
        except Error:
            pass
        self.curs.execute("""SELECT id FROM users WHERE username = ?""", (username,))
        self.user_id = (self.curs.fetchone())[0]

        # ============== Image using tkinter =====================
        self.index = PhotoImage(file="Photos/index_gif.gif")
        self.index = self.index.subsample(20, 20)
        self.label = Label(image=self.index)
        self.label.grid(row=0, column=0, sticky=NW)

        self.b_label = Label(text="Order Pizza")
        self.b_label.grid(row=0, column=1, columnspan=3, sticky=S)

        # ====================== Images =======================================
        self.chicken_ranch = PhotoImage(file="Photos/chicken_ranch.gif")
        self.pepperoni = PhotoImage(file="Photos/pepperoni.gif")
        self.havai = PhotoImage(file="Photos/havai.gif")
        # ====================== Image Labels ====================================
        self.ranch_label = Label(image=self.chicken_ranch)
        self.ch_label = Label(text="Chicken Ranch")
        self.ranch_label.grid(row=2, column=0, sticky=SW, padx=4, pady=4)
        self.ch_label.grid(row=3, column=0, sticky=S, padx=4, pady=4)

        self.pepperoni_label = Label(image=self.pepperoni)
        self.pep_label = Label(text="Pepperoni")
        self.pepperoni_label.grid(row=2, column=1, sticky=SW, padx=4, pady=4)
        self.pep_label.grid(row=3, column=1, sticky=S, padx=4, pady=4)

        self.hawaii_label = Label(image=self.havai)
        self.haw_label = Label(text="Hawaii")
        self.hawaii_label.grid(row=2, column=2, sticky=SW, padx=4, pady=4)
        self.haw_label.grid(row=3, column=2, sticky=S, padx=4, pady=4)

        # ===================== Change Ingredients Buttons =====================================
        self.curs.execute("""SELECT receipt FROM pizzas WHERE name='Chicken Ranch'""")
        self.r_r = self.curs.fetchone()
        self.ranch_receipt = Label(text=str(self.r_r), bg="#ffffcc")
        self.ranch_receipt.grid(row=4, column=0, sticky=S, padx=4, pady=4)
        self.curs.execute("""SELECT receipt FROM pizzas WHERE name='Pepperoni'""")
        self.p_r = self.curs.fetchone()
        self.pep_receipt = Label(text=str(self.p_r), bg="#ffffcc")
        self.pep_receipt.grid(row=4, column=1, sticky=S, padx=4, pady=4)
        self.curs.execute("""SELECT receipt FROM pizzas WHERE name='Hawaii'""")
        self.h_r = self.curs.fetchone()
        self.haw_receipt = Label(text=str(self.h_r), bg="#ffffcc")
        self.haw_receipt.grid(row=4, column=2, sticky=S, padx=4, pady=4)
        # ====================== Choose Buttons ==========================================================
        self.ranch_add = Button(text="Choose these",
                                command=lambda: {self.choose_window('Chicken Ranch', self.user_id)})
        self.ranch_add.grid(row=5, column=0, sticky=S, padx=4, pady=4)

        self.pep_add = Button(text="Choose these", command=lambda: {self.choose_window('Pepperoni', self.user_id)})
        self.pep_add.grid(row=5, column=1, sticky=S, padx=4, pady=4)

        self.haw_add = Button(text="Choose these", command=lambda: {self.choose_window('Hawaii', self.user_id)})
        self.haw_add.grid(row=5, column=2, sticky=S, padx=4, pady=4)
        # ======================== Clear Card Buttons ==================================================
        self.checkout = Button(text="Go to Checkout page >>", command= lambda : {self.checkout_page(self.user_id)})
        self.checkout.grid(row=8, column=2, sticky=SE, padx=10, pady=10)

        self.clear = Button(text="Clear Card", command=lambda: {self.clear_card(self.user_id)})
        self.clear.grid(row=9, column=2, sticky=SE, padx=10, pady=10)

    ## THINK HOW TO WRITE TO CARD DB CHANGED RECEIPTS

    def choose_window(self, pizza_name, user_id):
        self.top = Toplevel(self.root1)
        ChoosePizza(self.top, pizza_name, user_id)

    def checkout_page(self, user_id):
        self.root1.destroy()
        Pizza_Checkout.checkout(user_id)

    def clear_card(self, user_id):
        self.curs.execute("""DELETE FROM card WHERE user_id=?""", (user_id, ))
        self.con.commit()

class ChoosePizza:

    def __init__(self, master, pizza_name, user_id):
        self.root = master
        self.root.geometry("430x500+100+100")
        self.root.grid()
        # self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.connection = sqlite3.connect('pizza.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""SELECT receipt, price, photo from pizzas WHERE name=?""", (pizza_name,))
        self.pizza = self.cursor.fetchone()
        self.pizza_price = int(self.pizza[1])
        self.pizza_receipt = str(self.pizza[0])
        self.image = PhotoImage(file=self.pizza[2])
        self.label = Label(self.root, image=self.image)
        self.label.photo = self.image
        self.label.grid(row=0, column=0, sticky=S, padx=4, pady=4)
        self.pizza_name = Label(self.root, text=pizza_name)
        self.pizza_name.grid(row=1, column=0, sticky=S, padx=4, pady=4)
        self.change_button = Button(self.root, text="Add Ingredients -->", width=25, command=lambda :{self.change_ingredients(pizza_name)})
        self.change_button.grid(row=2, column=0, sticky=S, padx=4, pady=4)
        self.pizza_price_label = Label(self.root, text="Price: $" + str(self.pizza[1]))
        self.pizza_price_label.grid(row=3, column=0, sticky=S, padx=4, pady=4)

        self.add_button = Button(self.root, text="Add to Card", command=lambda: {self.add_to_card(pizza_name, user_id)})
        self.add_button.grid(row=3, column=1, columnspan=2, sticky=W, padx=4, pady=4)

    def change_ingredients(self, pizza_name):
        self.root.geometry("730x500+100+100")
        self.close = Button(self.root, text="Save Changes", width=25, command=self.save_changes)
        self.close.grid(row=2, column=0, sticky=S, padx=4, pady=4)
        # check_buttons:
        self.cheese_button = Button(self.root, text=" Add Cheese", command=lambda: {self.add_extension(1.4, 'cheese')})
        self.cheese_button.grid(row=1, column=2, sticky=S, padx=4, pady=4)
        self.ketchup_button = Button(self.root, text=" Add Ketchup", command=lambda: {self.add_extension(1.3, 'ketchup')})
        self.ketchup_button.grid(row=2, column=2, sticky=S, padx=4, pady=4)
        self.bbq_button = Button(self.root, text=" Add barbecue sauce", command=lambda: {self.add_extension(1.2, 'barbecue sauce')})
        self.bbq_button.grid(row=3, column=2, sticky=S, padx=4, pady=4)
        self.sausage_button = Button(self.root, text="Add Sausage", command=lambda: {self.add_extension(1.4, 'sausage')})
        self.sausage_button.grid(row=4, column=2, sticky=S, padx=4, pady=4)
        self.olives_button = Button(self.root, text="Add Olives", command=lambda: {self.add_extension(1.0, 'olives')})
        self.olives_button.grid(row=5, column=2, sticky=S, padx=4, pady=4)

    def save_changes(self):
        self.root.geometry("430x500+100+100")
        self.close.destroy()
        self.sausage_button.destroy()
        self.bbq_button.destroy()
        self.olives_button.destroy()
        # self.pineapple_button.destroy()
        self.cheese_button.destroy()
        self.ketchup_button.destroy()
        # self.message.destroy()


    def add_to_card(self, pizza_name, user_id):
        row_num = self.cursor.execute("""SELECT * FROM card""").rowcount + 2
        print(row_num)
        self.cursor.execute("""INSERT INTO card VALUES(?, ?, ?, ?, ?)""",
                        (None, user_id, pizza_name, self.pizza_receipt, self.pizza_price,))
        self.connection.commit()
        self.message = Message(self.root, text="Added to Cart")
        self.message.grid(row=4, column=1, columnspan=2, padx=4, pady=4)
        self.root.after(1200, self.clear_message)

    def add_extension(self, extension_price, extension):
        if extension == '0':
            pass
        self.pizza_receipt = self.pizza_receipt + ', ' + str(extension)
        self.pizza_price = int(self.pizza[1]) + extension_price
        self.message = Message(self.root, text="Added "+str(extension))
        self.message.grid(row=4, column=3, padx=4, pady=4)
        self.root.after(1200, self.clear_message)

    def clear_message(self):
        self.message.destroy()


def order(username):
    conn = sqlite3.connect('pizza.db')
    root = Tk()
    root.title("Messy Pizza App")
    root.geometry("1000x600+150+30")
    root.configure(bg="#ffcc99")
    my_gui = PizzaOrder(root, username, conn)
    root.mainloop()





        # self.pineapple = BooleanVar()
        # self.pineapple_button = Checkbutton(self.root, text="Pineapple")
        # self.pineapple_button.grid(row=4, column=2, sticky=S, padx=4, pady=4)

