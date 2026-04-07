# app.py - Main Streamlit Application

import streamlit as st
from datetime import datetime, timedelta, date
import pandas as pd
from book_module import Book, PremiumBook, generate_rental_id, calculate_late_fee, total_rentals

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

# ==================== HOME PAGE ====================
if menu == "🏠 Home":
    st.header("🏠 Welcome to Book Renting System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📚 Available Books", len([b for b in st.session_state.books.values() if not b.is_rented]))
    with col2:
        st.metric("🔄 Total Rentals", total_rentals)
    with col3:
        st.metric("⭐ Premium Books", len([b for b in st.session_state.books.values() if isinstance(b, PremiumBook)]))
    
    st.markdown("---")
    st.subheader("🌟 Features")
    st.info("""
    ✅ **Function Implementation** - Generate Rental ID & Calculate Late Fee
    ✅ **Class & Object** - Book class with 4+ attributes and methods
    ✅ **Module Implementation** - Separate module file (book_module.py)
    ✅ **Inheritance** - PremiumBook inherits from Book with discount feature
    ✅ **Function Overloading** - calculate_rental_cost() with default parameter
    ✅ **Exception Handling** - Handles invalid and empty inputs
    ✅ **Streamlit GUI** - Complete interactive interface
    """)

# ==================== BROWSE BOOKS ====================
elif menu == "📚 Browse Books":
    st.header("📚 Available Books")
    
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
    selected_book_id = st.selectbox("Select a book to view details:", list(st.session_state.books.keys()))
    
    if selected_book_id:
        book = st.session_state.books[selected_book_id]
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {book.title}")
                st.write(f"**Author:** {book.author}")
                st.write(f"**Price per day:** RM{book.rental_price_per_day}")
            with col2:
                st.write(f"**Status:** {'Rented' if book.is_rented else 'Available'}")
                st.write(f"**Type:** {'Premium Member Book' if isinstance(book, PremiumBook) else 'Regular Book'}")
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
            
            # Additional input: Member type
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
                    
                    # Apply discount logic based on member type
                    if member_type == "Premium" and isinstance(book, PremiumBook):
                        cost = book.calculate_rental_cost(rental_days, apply_discount=True)
                        discount_msg = " (with 20% premium discount applied!)"
                    else:
                        cost = book.calculate_rental_cost(rental_days, apply_discount=False)
                        discount_msg = ""
                    
                    # Generate rental ID using function
                    rental_id = generate_rental_id()
                    due_date = date.today() + timedelta(days=rental_days)
                    
                    # Create rental record
                    rental_record = {
                        "rental_id": rental_id,
                        "book_id": selected_book,
                        "book_title": book.title,
                        "customer": customer_name,
                        "rental_days": rental_days,
                        "total_cost": cost,
                        "rental_date": date.today(),
                        "due_date": due_date,
                        "status": "Active"
                    }
                    
                    st.session_state.rentals.append(rental_record)
                    book.rent_book()
                    st.session_state.current_rental = rental_record
                    
                    # Display success message
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>✅ Rental Successful!</h3>
                        <p><strong>Rental ID:</strong> {rental_id}</p>
                        <p><strong>Book:</strong> {book.title}</p>
                        <p><strong>Customer:</strong> {customer_name}</p>
                        <p><strong>Total Cost:</strong> RM{cost}{discount_msg}</p>
                        <p><strong>Due Date:</strong> {due_date}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except ValueError as ve:
                    st.error(f"❌ Input Error: {str(ve)}")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")

# ==================== RETURN BOOK ====================
elif menu == "🔄 Return Book":
    st.header("🔄 Return a Book")
    
    active_rentals = [r for r in st.session_state.rentals if r['status'] == 'Active']
    
    if not active_rentals:
        st.info("No active rentals to return.")
    else:
        rental_options = {i: f"{r['rental_id']} - {r['book_title']} (Due: {r['due_date']})" 
                         for i, r in enumerate(active_rentals)}
        
        selected_index = st.selectbox("Select rental to return:", options=list(rental_options.keys()),
                                      format_func=lambda x: rental_options[x])
        
        # INPUT: Return date
        return_date = st.date_input("📅 Return Date", value=date.today())
        
        if st.button("🔄 Process Return"):
            try:
                rental = active_rentals[selected_index]
                
                # Calculate late fee using function
                late_fee = calculate_late_fee(return_date, rental['due_date'])
                
                total_payment = rental['total_cost'] + late_fee
                
                # Update status
                rental['status'] = 'Returned'
                rental['return_date'] = return_date
                rental['late_fee'] = late_fee
                
                # Update book availability
                st.session_state.books[rental['book_id']].return_book()
                
                # Display return summary
                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Book Returned Successfully!</h3>
                    <p><strong>Book:</strong> {rental['book_title']}</p>
                    <p><strong>Customer:</strong> {rental['customer']}</p>
                    <p><strong>Rental Cost:</strong> RM{rental['total_cost']}</p>
                    <p><strong>Late Fee:</strong> RM{late_fee}</p>
                    <p><strong>Total Payment:</strong> RM{total_payment}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error processing return: {str(e)}")

# ==================== RENTAL HISTORY ====================
elif menu == "📊 Rental History":
    st.header("📊 Rental History")
    
    if not st.session_state.rentals:
        st.info("No rental records found.")
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rentals", len(st.session_state.rentals))
        with col2:
            active = len([r for r in st.session_state.rentals if r['status'] == 'Active'])
            st.metric("Active Rentals", active)
        with col3:
            total_revenue = sum([r['total_cost'] for r in st.session_state.rentals])
            st.metric("Total Revenue", f"RM{total_revenue}")

# ==================== ABOUT PAGE ====================
elif menu == "ℹ️ About":
    st.header("ℹ️ About This System")
    
    st.markdown("""
    <div class="info-box">
        <h3>📋 Assignment Requirements Checklist</h3>
        <ul>
            <li>✅ <strong>Function Implementation:</strong> generate_rental_id(), calculate_late_fee()</li>
            <li>✅ <strong>Class & Object:</strong> Book class with 4+ attributes and 2+ methods</li>
            <li>✅ <strong>Module Implementation:</strong> All classes/functions in book_module.py</li>
            <li>✅ <strong>Inheritance:</strong> PremiumBook inherits from Book</li>
            <li>✅ <strong>Function Overloading:</strong> calculate_rental_cost(apply_discount=True/False)</li>
            <li>✅ <strong>GUI with Streamlit:</strong> text_input, number_input, selectbox, button</li>
            <li>✅ <strong>Exception Handling:</strong> try-except for empty/invalid inputs</li>
            <li>✅ <strong>Creativity:</strong> Complete book rental management system</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🛠️ Technologies Used")
    st.code("""
    - Python 3.x
    - Streamlit (GUI Framework)
    - Pandas (Data Display)
    - Datetime (Date Handling)
    """)