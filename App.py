# app.py - Complete Book Renting System (All in One File)

import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
import random

# ==================== MODULE SECTION (Functions & Classes) ====================

# Global variable to track total rentals
total_rentals = 0

# FUNCTION 1: Generate unique rental ID
def generate_rental_id():
    """Generate a unique rental ID"""
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


# ==================== STREAMLIT UI SECTION ====================

# Page Configuration
st.set_page_config(
    page_title="📚 Book Renting System",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        background-color: #2E4053;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .success-box {
        background-color: #D5F5E3;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28B463;
    }
    .error-box {
        background-color: #FADBD8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #E74C3C;
    }
    .info-box {
        background-color: #D6EAF8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3498DB;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'books' not in st.session_state:
        # Create sample books
        st.session_state.books = {
            "B001": Book("B001", "Python Programming", "John Smith", 2.50),
            "B002": Book("B002", "Data Science Handbook", "Jane Doe", 3.00),
            "B003": PremiumBook("B003", "AI Revolution", "Alan Turing", 4.00, True),
            "B004": PremiumBook("B004", "Cloud Computing", "Tim Berners", 3.50, False),
            "B005": Book("B005", "Web Development", "Mark Anderson", 2.00),
            "B006": PremiumBook("B006", "Machine Learning Basics", "Andrew Ng", 5.00, True),
        }
    if 'rentals' not in st.session_state:
        st.session_state.rentals = []
    if 'current_rental' not in st.session_state:
        st.session_state.current_rental = None

# Call the initialization
init_session_state()

# Header
st.markdown('<div class="main-header"><h1>📚 Book Renting System</h1><p>Rent your favorite books easily!</p></div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1674/1674805.png", width=100)
    st.title("📖 Menu")
    menu = st.radio("Choose Option:", ["🏠 Home", "📚 Browse Books", "💰 Rent a Book", "🔄 Return Book", "📊 Rental History", "ℹ️ About"])
    st.markdown("---")
    st.caption(f"Total Rentals: {total_rentals}")
    st.caption(f"Active Rentals: {len([r for r in st.session_state.rentals if r.get('status') == 'Active'])}")

# ==================== HOME PAGE ====================
if menu == "🏠 Home":
    st.header("🏠 Welcome to Book Renting System")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        available_count = len([b for b in st.session_state.books.values() if not b.is_rented])
        st.metric("📚 Available Books", available_count)
    with col2:
        st.metric("🔄 Total Rentals", total_rentals)
    with col3:
        premium_count = len([b for b in st.session_state.books.values() if isinstance(b, PremiumBook)])
        st.metric("⭐ Premium Books", premium_count)
    with col4:
        active_rentals = len([r for r in st.session_state.rentals if r.get('status') == 'Active'])
        st.metric("🔄 Active Rentals", active_rentals)
    
    st.markdown("---")
    st.subheader("🌟 Features Implemented")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>✅ Technical Requirements</h4>
            <ul>
                <li><strong>2 Functions</strong> - generate_rental_id(), calculate_late_fee()</li>
                <li><strong>Class & Object</strong> - Book class with 4+ attributes & 2+ methods</li>
                <li><strong>Module Implementation</strong> - All in one file (acts as module)</li>
                <li><strong>Inheritance</strong> - PremiumBook inherits from Book</li>
                <li><strong>Function Overloading</strong> - calculate_rental_cost() with default parameter</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>✅ GUI Requirements</h4>
            <ul>
                <li><strong>3+ Inputs</strong> - selectbox, text_input, number_input, date_input</li>
                <li><strong>Exception Handling</strong> - try-except for invalid/empty inputs</li>
                <li><strong>Streamlit Components</strong> - All widgets used properly</li>
                <li><strong>Output Display</strong> - Clear formatted results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🎯 System Features")
    st.info("""
    ✨ **Complete Book Rental Management System** - Rent books, calculate costs with premium discounts, track rental history, and manage returns with late fee calculation.
    """)

# ==================== BROWSE BOOKS ====================
elif menu == "📚 Browse Books":
    st.header("📚 Browse Available Books")
    
    # Create dataframe for display
    books_data = []
    for book_id, book in st.session_state.books.items():
        books_data.append({
            "ID": book_id,
            "Title": book.title,
            "Author": book.author,
            "Price/Day": f"RM{book.rental_price_per_day}",
            "Status": "❌ Rented" if book.is_rented else "✅ Available",
            "Type": "⭐ Premium" if isinstance(book, PremiumBook) else "📘 Regular"
        })
    
    df = pd.DataFrame(books_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("📖 Book Details")
    
    # Filter to show only available books for selection
    available_books = {bid: book for bid, book in st.session_state.books.items()}
    selected_book_id = st.selectbox("Select a book to view details:", list(available_books.keys()))
    
    if selected_book_id:
        book = st.session_state.books[selected_book_id]
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {book.title}")
                st.write(f"**Author:** {book.author}")
                st.write(f"**Price per day:** RM{book.rental_price_per_day}")
            with col2:
                st.write(f"**Status:** {'🔴 Rented' if book.is_rented else '🟢 Available'}")
                st.write(f"**Type:** {'⭐ Premium Member Book' if isinstance(book, PremiumBook) else '📘 Regular Book'}")
                if isinstance(book, PremiumBook) and book.is_premium_member:
                    st.success("⭐ 20% discount available for premium members!")

# ==================== RENT A BOOK ====================
elif menu == "💰 Rent a Book":
    st.header("💰 Rent a Book")
    
    with st.form("rental_form"):
        # INPUT 1: Select Book (using selectbox)
        available_books = {bid: book for bid, book in st.session_state.books.items() if not book.is_rented}
        
        if not available_books:
            st.error("❌ No books available for rent right now!")
        else:
            book_options = {bid: f"{book.title} by {book.author} (RM{book.rental_price_per_day}/day)" 
                           for bid, book in available_books.items()}
            selected_book = st.selectbox("📖 Select a Book", options=list(book_options.keys()), 
                                        format_func=lambda x: book_options[x])
            
            # INPUT 2: Customer Name (using text_input)
            customer_name = st.text_input("👤 Customer Name", placeholder="Enter your full name")
            
            # INPUT 3: Rental Days (using number_input)
            rental_days = st.number_input("📅 Number of Days", min_value=1, max_value=30, value=3, step=1)
            
            # INPUT 4: Member type (using selectbox)
            member_type = st.selectbox("⭐ Membership Type", ["Regular", "Premium"])
            
            submitted = st.form_submit_button("💰 Calculate & Rent")
            
            if submitted:
                # EXCEPTION HANDLING: Validate inputs
                try:
                    if not customer_name.strip():
                        raise ValueError("Customer name cannot be empty!")
                    
                    if rental_days <= 0:
                        raise ValueError("Rental days must be at least 1!")
                    
                    book = st.session_state.books[selected_book]
                    
                    # FUNCTION OVERLOADING DEMONSTRATION
                    # calculate_rental_cost with and without discount
                    if member_type == "Premium" and isinstance(book, PremiumBook):
                        # With discount (apply_discount=True by default)
                        cost = book.calculate_rental_cost(rental_days, apply_discount=True)
                        discount_msg = " (with 20% premium discount applied!)"
                    else:
                        # Without discount
                        cost = book.calculate_rental_cost(rental_days, apply_discount=False)
                        discount_msg = ""
                    
                    # Generate rental ID using FUNCTION 1
                    rental_id = generate_rental_id()
                    due_date = date.today() + timedelta(days=rental_days)
                    
                    # Create rental record (OBJECT instantiation and usage)
                    rental_record = {
                        "rental_id": rental_id,
                        "book_id": selected_book,
                        "book_title": book.title,
                        "customer": customer_name,
                        "rental_days": rental_days,
                        "total_cost": cost,
                        "rental_date": date.today(),
                        "due_date": due_date,
                        "status": "Active",
                        "member_type": member_type
                    }
                    
                    st.session_state.rentals.append(rental_record)
                    book.rent_book()  # Using class method
                    st.session_state.current_rental = rental_record
                    
                    # Display success message
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>✅ Rental Successful!</h3>
                        <p><strong>Rental ID:</strong> {rental_id}</p>
                        <p><strong>Book:</strong> {book.title}</p>
                        <p><strong>Customer:</strong> {customer_name}</p>
                        <p><strong>Rental Days:</strong> {rental_days} days</p>
                        <p><strong>Total Cost:</strong> RM{cost}{discount_msg}</p>
                        <p><strong>Due Date:</strong> {due_date}</p>
                        <p><strong>Membership:</strong> {member_type}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except ValueError as ve:
                    st.error(f"❌ Input Error: {str(ve)}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")

# ==================== RETURN BOOK ====================
elif menu == "🔄 Return Book":
    st.header("🔄 Return a Book")
    
    active_rentals = [r for r in st.session_state.rentals if r.get('status') == 'Active']
    
    if not active_rentals:
        st.info("ℹ️ No active rentals to return.")
    else:
        rental_options = {i: f"{r['rental_id']} - {r['book_title']} (Due: {r['due_date']})" 
                         for i, r in enumerate(active_rentals)}
        
        selected_index = st.selectbox("Select rental to return:", options=list(rental_options.keys()),
                                      format_func=lambda x: rental_options[x])
        
        # INPUT: Return date (using date_input)
        return_date = st.date_input("📅 Return Date", value=date.today())
        
        if st.button("🔄 Process Return"):
            try:
                rental = active_rentals[selected_index]
                
                # Calculate late fee using FUNCTION 2
                late_fee = calculate_late_fee(return_date, rental['due_date'])
                
                total_payment = rental['total_cost'] + late_fee
                
                # Update status
                rental['status'] = 'Returned'
                rental['return_date'] = return_date
                rental['late_fee'] = late_fee
                
                # Update book availability (using class method)
                st.session_state.books[rental['book_id']].return_book()
                
                # Display return summary
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Book Returned Successfully!</h3>
                    <p><strong>Rental ID:</strong> {rental['rental_id']}</p>
                    <p><strong>Book:</strong> {rental['book_title']}</p>
                    <p><strong>Customer:</strong> {rental['customer']}</p>
                    <p><strong>Rental Cost:</strong> RM{rental['total_cost']}</p>
                    <p><strong>Late Fee:</strong> RM{late_fee}</p>
                    <p><strong>Total Payment:</strong> RM{total_payment}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error processing return: {str(e)}")

# ==================== RENTAL HISTORY ====================
elif menu == "📊 Rental History":
    st.header("📊 Rental History")
    
    if not st.session_state.rentals:
        st.info("ℹ️ No rental records found.")
    else:
        # Create dataframe for display
        history_data = []
        for rental in st.session_state.rentals:
            history_data.append({
                "Rental ID": rental['rental_id'],
                "Book": rental['book_title'],
                "Customer": rental['customer'],
                "Rental Date": rental['rental_date'],
                "Due Date": rental['due_date'],
                "Cost": f"RM{rental['total_cost']}",
                "Status": rental['status'],
                "Late Fee": f"RM{rental.get('late_fee', 0)}"
            })
        
        df_history = pd.DataFrame(history_data)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        # Statistics
        st.markdown("---")
        st.subheader("📈 Rental Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rentals", len(st.session_state.rentals))
        with col2:
            active = len([r for r in st.session_state.rentals if r.get('status') == 'Active'])
            st.metric("Active Rentals", active)
        with col3:
            completed = len([r for r in st.session_state.rentals if r.get('status') == 'Returned'])
            st.metric("Completed Rentals", completed)
        with col4:
            total_revenue = sum([r['total_cost'] for r in st.session_state.rentals])
            st.metric("Total Revenue", f"RM{total_revenue}")

# ==================== ABOUT PAGE ====================
elif menu == "ℹ️ About":
    st.header("ℹ️ About This System")
    
    st.markdown("""
    <div class="info-box">
        <h3>📋 Assignment Requirements Checklist - DFK50083 Python Programming</h3>
        <h4>✅ All Requirements Met:</h4>
        <ul>
            <li><strong>✅ Function Implementation (2 functions):</strong><br/>
                - generate_rental_id() - Generates unique rental ID<br/>
                - calculate_late_fee() - Calculates late fees for overdue returns</li>
            <li><strong>✅ Class and Object Implementation:</strong><br/>
                - Book class with 5 attributes (book_id, title, author, rental_price_per_day, is_rented)<br/>
                - 4 methods (calculate_rental_cost, display_info, rent_book, return_book)<br/>
                - Objects created and used throughout the system</li>
            <li><strong>✅ Module Implementation:</strong><br/>
                - All classes and functions in single file (acts as complete module)</li>
            <li><strong>✅ Inheritance:</strong><br/>
                - PremiumBook subclass inherits from Book with 20% discount feature</li>
            <li><strong>✅ Function Overloading Concept:</strong><br/>
                - calculate_rental_cost(days, apply_discount=True/False) with default parameter</li>
            <li><strong>✅ GUI with Streamlit:</strong><br/>
                - text_input, number_input, selectbox, date_input, button, form</li>
            <li><strong>✅ Exception Handling:</strong><br/>
                - try-except blocks for empty inputs and invalid values<br/>
                - st.error() for displaying error messages</li>
            <li><strong>✅ Creativity & Functionality:</strong><br/>
                - Complete book rental management system with rental tracking, late fees, premium discounts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🛠️ Technologies Used")
    st.code("""
    - Python 3.x
    - Streamlit (GUI Framework)
    - Pandas (Data Display and Tables)
    - Datetime (Date Handling and Calculations)
    - Random (ID Generation)
    """)
    
    st.markdown("---")
    st.subheader("🎯 How to Use This System")
    st.markdown("""
    1. **Browse Books** - View all available books with their details
    2. **Rent a Book** - Select a book, enter customer details, and calculate rental cost
    3. **Return Book** - Process returns and calculate late fees if applicable
    4. **Rental History** - View all past and active rentals
    5. **Premium Discount** - Premium members get 20% discount on premium books
    """)
    
    st.markdown("---")
    st.subheader("📞 Contact")
    st.info("**Developer:** Student - DFK50083 Python Programming\n\n**Assessment:** Problem Based Assignment - Topic 2 & 3")

# ==================== END OF FILE ====================