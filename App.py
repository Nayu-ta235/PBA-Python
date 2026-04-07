# app.py - Simple Streamlit GUI

import streamlit as st
from datetime import date, timedelta
from book_module import Book, PremiumBook, generate_rental_id, calculate_late_fee

# Page setup
st.set_page_config(page_title="Book Rental", page_icon="📚")

st.title("📚 Simple Book Renting System")

# Initialize data
if 'books' not in st.session_state:
    st.session_state.books = {
        "B001": Book("B001", "Python Programming", "John Smith", 2.50),
        "B002": PremiumBook("B002", "AI Revolution", "Alan Turing", 4.00),
        "B003": Book("B003", "Web Development", "Mark Lee", 2.00),
    }

if 'rentals' not in st.session_state:
    st.session_state.rentals = []

# Sidebar menu
menu = st.sidebar.radio("Menu", ["📖 Browse Books", "💰 Rent Book", "🔄 Return Book", "📊 History"])

# ========== BROWSE BOOKS ==========
if menu == "📖 Browse Books":
    st.subheader("Available Books")
    
    for book_id, book in st.session_state.books.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{book.title}** - {book.author}")
            st.caption(f"RM{book.price}/day")
            if isinstance(book, PremiumBook):
                st.caption("⭐ Premium (20% discount)")
        with col2:
            if book.is_rented:
                st.error("Rented")
            else:
                st.success("Available")
        st.divider()

# ========== RENT BOOK ==========
elif menu == "💰 Rent Book":
    st.subheader("Rent a Book")
    
    # Get available books
    available_books = {bid: b for bid, b in st.session_state.books.items() if not b.is_rented}
    
    if available_books:
        # Input fields
        selected = st.selectbox("Choose Book", list(available_books.keys()), 
                               format_func=lambda x: available_books[x].title)
        
        customer_name = st.text_input("Your Name")
        
        days = st.number_input("Number of Days", min_value=1, max_value=30, value=3)
        
        member_type = st.radio("Member Type", ["Regular", "Premium"])
        
        if st.button("Rent Book"):
            try:
                # Validation
                if not customer_name:
                    st.error("Please enter your name!")
                else:
                    book = st.session_state.books[selected]
                    
                    # Calculate cost
                    if member_type == "Premium" and isinstance(book, PremiumBook):
                        cost = book.calculate_cost(days, apply_discount=True)
                        st.info("✨ Premium discount applied!")
                    else:
                        cost = book.calculate_cost(days, apply_discount=False)
                    
                    # Create rental record
                    rental_id = generate_rental_id()
                    due_date = date.today() + timedelta(days=days)
                    
                    st.session_state.rentals.append({
                        "id": rental_id,
                        "book": book.title,
                        "customer": customer_name,
                        "days": days,
                        "cost": cost,
                        "rental_date": date.today(),
                        "due_date": due_date,
                        "status": "Active"
                    })
                    
                    book.is_rented = True
                    
                    # Show success
                    st.success(f"✅ Rental Successful!")
                    st.write(f"**Rental ID:** {rental_id}")
                    st.write(f"**Total Cost:** RM{cost}")
                    st.write(f"**Due Date:** {due_date}")
                    
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("No books available for rent!")

# ========== RETURN BOOK ==========
elif menu == "🔄 Return Book":
    st.subheader("Return a Book")
    
    active_rentals = [r for r in st.session_state.rentals if r['status'] == "Active"]
    
    if active_rentals:
        # Select rental to return
        rental_options = {i: f"{r['book']} - {r['customer']}" for i, r in enumerate(active_rentals)}
        selected_idx = st.selectbox("Select Rental", list(rental_options.keys()), 
                                    format_func=lambda x: rental_options[x])
        
        return_date = st.date_input("Return Date", date.today())
        
        if st.button("Process Return"):
            rental = active_rentals[selected_idx]
            
            # Calculate late fee
            late_fee = calculate_late_fee(return_date, rental['due_date'])
            total = rental['cost'] + late_fee
            
            # Update status
            rental['status'] = "Returned"
            
            # Make book available again
            for book in st.session_state.books.values():
                if book.title == rental['book']:
                    book.is_rented = False
                    break
            
            # Show summary
            st.success(f"✅ Book Returned!")
            st.write(f"**Rental Cost:** RM{rental['cost']}")
            st.write(f"**Late Fee:** RM{late_fee}")
            st.write(f"**Total Paid:** RM{total}")
    else:
        st.info("No active rentals to return")

# ========== HISTORY ==========
elif menu == "📊 History":
    st.subheader("Rental History")
    
    if st.session_state.rentals:
        for r in st.session_state.rentals:
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{r['book']}** - {r['customer']}")
                    st.caption(f"ID: {r['id']}")
                with col2:
                    st.write(f"Cost: RM{r['cost']}")
                    status = "✅ Returned" if r['status'] == "Returned" else "🔄 Active"
                    st.caption(status)
                st.divider()
    else:
        st.info("No rental history")