# book_module.py - Module containing classes and functions

import datetime
import random

# Global variable to track total rentals
total_rentals = 0

# FUNCTION 1: Generate unique rental ID
def generate_rental_id():
    """Generate a unique rental ID"""
    import random
    return f"RENT-{random.randint(1000, 9999)}"

# FUNCTION 2: Calculate late fee
def calculate_late_fee(return_date, due_date, fee_per_day=1.50):
    """Calculate late fee for overdue books"""
    if return_date <= due_date:
        return 0
    days_late = (return_date - due_date).days
    return days_late * fee_per_day

# Base Class
class Book:
    """Base class for books"""
    
    # Class attribute
    rental_counter = 0
    
    def __init__(self, book_id, title, author, rental_price_per_day):
        """Initialize book with 4 attributes"""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.rental_price_per_day = rental_price_per_day
        self.is_rented = False
    
    # Method 1: Calculate rental cost (processing method)
    def calculate_rental_cost(self, days):
        """Calculate total rental cost"""
        global total_rentals
        if days <= 0:
            return 0
        total = self.rental_price_per_day * days
        Book.rental_counter += 1
        total_rentals += 1
        return total
    
    # Method 2: Display book info
    def display_info(self):
        """Display book information"""
        return f"📖 {self.title} by {self.author} (ID: {self.book_id}) - RM{self.rental_price_per_day}/day"
    
    def rent_book(self):
        """Mark book as rented"""
        self.is_rented = True
    
    def return_book(self):
        """Mark book as returned"""
        self.is_rented = False


# Subclass with Inheritance
class PremiumBook(Book):
    """Subclass for premium books with special features"""
    
    def __init__(self, book_id, title, author, rental_price_per_day, is_premium_member=True):
        super().__init__(book_id, title, author, rental_price_per_day)
        self.is_premium_member = is_premium_member
        self.premium_discount = 0.20  # 20% discount
    
    # FUNCTION OVERLOADING CONCEPT using default parameter
    def calculate_rental_cost(self, days, apply_discount=True):
        """
        Function Overloading Concept:
        - Without parameter (apply_discount=True) -> applies discount
        - With parameter apply_discount=False -> normal calculation
        """
        base_cost = super().calculate_rental_cost(days)
        
        if apply_discount and self.is_premium_member:
            discounted_cost = base_cost * (1 - self.premium_discount)
            return round(discounted_cost, 2)
        return base_cost
    
    def display_info(self):
        """Override display info for premium books"""
        basic_info = super().display_info()
        if self.is_premium_member:
            return basic_info + " ⭐ (20% discount for premium members)"
        return basic_info