import sqlite3
from sqlite3 import Error
from Pizza import PizzaBuilder
import datetime

class PizzaWrite(PizzaBuilder):
    def __init__(self, pizza_type):
        super().__init__(pizza_type)
        self.con = sqlite3.connect('pizza.db')
        self.cursor = self.con.cursor()
        #self.i = 1
        try:
            self.cursor.execute("""CREATE TABLE users(id integer PRIMARY KEY, username text, password text)""")
        except Error:
            pass
        try:
            self.cursor.execute("""INSERT INTO users VALUES(?, ?, ?)""", (None, "admin", "ucantguess", ))
            self.con.commit()
        except Error:
            pass
        try:
            self.cursor.execute("""CREATE TABLE history(username text, pizza_name text, receipt text, total_sum int, 
            time timestamp )""")
        except Error:
            pass
# ================= Chicken Ranch ================================
        self.c_pizza = PizzaBuilder(self.pizza_type)
        self.c_pizza.add_extension('Chicken')
        self.c_pizza.add_extension('Cheese')
        self.c_pizza.add_extension('Olive')
        self.c_pizza.add_extension('Mushroom')
        self.c_pizza.add_extension('BBQSauce')
        self.c_price = self.c_pizza.get_price()
        self.c_receipt = self.c_pizza.get_status()

        self.p_pizza = PizzaBuilder(self.pizza_type)
        self.p_pizza.add_extension('Sausage')
        self.p_pizza.add_extension('Cheese')
        self.p_pizza.add_extension('Ketchup')
        self.p_price = self.p_pizza.get_price()
        self.p_receipt = self.p_pizza.get_status()

        self.h_pizza = PizzaBuilder(self.pizza_type)
        self.h_pizza.add_extension('Pineapple')
        self.h_pizza.add_extension('Mozzarella')
        self.h_pizza.add_extension('Chicken')
        self.h_price = self.h_pizza.get_price()
        self.h_receipt = self.h_pizza.get_status()

        try:
            self.cursor.execute("""CREATE TABLE pizzas(id integer PRIMARY KEY, name text, receipt text, price float, 
            photo text)""")
        except Error:
            print("Error creating table")
        try:
            self.cursor.execute("""INSERT INTO pizzas VALUES(?, "Chicken Ranch", ?, ?,"Photos/chicken_ranch.gif")""",
                                (1, self.c_receipt, self.c_price,))
            self.cursor.execute("""INSERT INTO pizzas VALUES(?, "Pepperoni", ?, ?, "Photos/pepperoni.gif")""",
                                (2, self.p_receipt, self.p_price,))
            self.cursor.execute("""INSERT INTO pizzas VALUES(?, "Hawaii", ?, ?, "Photos/havai.gif")""",
                                (3, self.h_receipt, self.h_price,))
            self.con.commit()
        except Error:
            print("Error writing to db")

def generate():
    pizza = PizzaWrite('DefaultPizza')
