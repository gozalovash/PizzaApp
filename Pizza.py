from abc import *
import sqlite3


class Pizza(metaclass=ABCMeta):
    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_status(self):
        pass


class DefaultPizza(Pizza):

    def __init__(self):
        self.pizza_price = 1.0

    def get_price(self):
        return self.pizza_price

    def get_status(self):
        return " "


class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza = pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()


class Cheese(PizzaDecorator):
    def __init__(self, pizza):
        super(Cheese, self).__init__(pizza)
        self.__cheese_price = 1.4

    @property
    def price(self):
        return self.__cheese_price

    def get_price(self):
        return super(Cheese, self).get_price() + self.__cheese_price

    def get_status(self):
        return super(Cheese, self).get_status() + ", cheese"


class Sausage(PizzaDecorator):
    def __init__(self, pizza):
        super(Sausage, self).__init__(pizza)
        self.__sausage_price = 1.4

    @property
    def price(self):
        return self.__sausage_price

    def get_price(self):
        return super(Sausage, self).get_price() + self.__sausage_price

    def get_status(self):
        return super(Sausage, self).get_status() + ", sausage"


class Mushroom(PizzaDecorator):
    def __init__(self, pizza):
        super(Mushroom, self).__init__(pizza)
        self.__mushroom_price = 1.2

    @property
    def price(self):
        return self.__mushroom_price

    def get_price(self):
        return super(Mushroom, self).get_price() + self.__mushroom_price

    def get_status(self):
        return super(Mushroom, self).get_status() + ", mushroom"


class Pineapple(PizzaDecorator):
    def __init__(self, pizza):
        super(Pineapple, self).__init__(pizza)
        self.__pineapple_price = 1.4

    @property
    def price(self):
        return self.__pineapple_price

    def get_price(self):
        return super(Pineapple, self).get_price() + self.__pineapple_price

    def get_status(self):
        return super(Pineapple, self).get_status() + ", pineapple"


class Chicken(PizzaDecorator):
    def __init__(self, pizza):
        super(Chicken, self).__init__(pizza)
        self.__chicken_price = 1.4

    @property
    def price(self):
        return self.__chicken_price

    def get_price(self):
        return super(Chicken, self).get_price() + self.__chicken_price

    def get_status(self):
        return super(Chicken, self).get_status() + ", chicken"


class Ketchup(PizzaDecorator):
    def __init__(self, pizza):
        super(Ketchup, self).__init__(pizza)
        self.__ketchup_price = 1.3

    @property
    def price(self):
        return self.__ketchup_price

    def get_price(self):
        return super(Ketchup, self).get_price() + self.__ketchup_price

    def get_status(self):
        return super(Ketchup, self).get_status() + ", ketchup"


class Olive(PizzaDecorator):
    def __init__(self, pizza):
        super(Olive, self).__init__(pizza)
        self.__olive_price = 1.0

    @property
    def price(self):
        return self.__olive_price

    def get_price(self):
        return super(Olive, self).get_price() + self.__olive_price

    def get_status(self):
        return super(Olive, self).get_status() + ", olives"


class Mozzarella(PizzaDecorator):
    def __init__(self, pizza):
        super(Mozzarella, self).__init__(pizza)
        self.__mozzarella_price = 1.5

    @property
    def price(self):
        return self.__mozzarella_price

    def get_price(self):
        return super(Mozzarella, self).get_price() + self.__mozzarella_price

    def get_status(self):
        return super(Mozzarella, self).get_status() + ", mozzarella"


class BBQSauce(PizzaDecorator):
    def __init__(self, pizza):
        super(BBQSauce, self).__init__(pizza)
        self.__bbqSauce_price = 1.2

    @property
    def price(self):
        return self.__bbqSauce_price

    def get_price(self):
        return super(BBQSauce, self).get_price() + self.__bbqSauce_price

    def get_status(self):
        return super(BBQSauce, self).get_status() + ", barbecue sauce"


# _________________________________ BUILDER ___________________________________


class PizzaBuilder:

    def __init__(self, pizza_type):
        self.pizza_type = pizza_type
        self.pizza = eval(pizza_type)()
        self.extensions_list = []

    def add_extension(self, extension):
        self.pizza = eval(extension)(self.pizza)
        self.extensions_list.append(extension)

    def remove_extension(self, extension):
        if extension in self.extensions_list:
            self.extensions_list.remove(extension)
        temp_pizza = eval(self.pizza_type)()
        for ex in self.extensions_list:
            temp_pizza = eval(ex)(temp_pizza)
        self.pizza = temp_pizza

    def get_price(self):
        return self.pizza.get_price()

    def get_status(self):
        return self.pizza.get_status()
