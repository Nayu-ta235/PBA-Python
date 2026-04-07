# book_module.py - Simple module with functions and classes

import random
from datetime import date, timedelta

# FUNCTION 1: Generate rental ID
def generate_rental_id():
    return f"RENT-{random.randint(1000, 9999)}"

# FUNCTION 2: Calculate late fee
def calculate_late_fee(return_date, due_date):
    if return_date <= due_date:
        return 0
    days_late = (return_date - due_date).days
    return days_late * 1.50

# CLASS 1: Book class
class Book:
    def __init__(self, book_id, title, author, price):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price
        self.is_rented = False
    
    def calculate_cost(self, days):
        return self.price * days
    
    def display_info(self):
        return f"{self.title} by {self.author} - RM{self.price}/day"

# CLASS 2: PremiumBook (Inheritance)
class PremiumBook(Book):
    def __init__(self, book_id, title, author, price):
        super().__init__(book_id, title, author, price)
        self.discount = 0.20
    
    # Function overloading with default parameter
    def calculate_cost(self, days, apply_discount=True):
        total = self.price * days
        if apply_discount:
            return round(total * (1 - self.discount), 2)
        return total