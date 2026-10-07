
import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Karishma Restaurant Bill Generator",
    page_icon="🍔",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #ff4b4b;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 25px;
    }

    .bill-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
    }

    .total {
        font-size: 28px;
        font-weight: bold;
        color: #ff4b4b;
        text-align: right;
    }

    .success {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: green;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- RESTAURANT MENU ----------------
menu = {
    "🍕 Pizza": 250,
    "🍔 Burger": 150,
    "🍟 French Fries": 100,
    "🌮 Taco": 120,
    "🍝 Pasta": 180,
    "🥪 Sandwich": 130,
    "🍗 Chicken Biryani": 220,
    "🥤 Cold Drink": 60,
    "🍦 Ice Cream": 80,
    "☕ Coffee": 70
}


# ---------------- HEADER ----------------
st.markdown(
    '<div class="title">🍔 Karishma Restaurant Bill Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Select your food items and generate your bill instantly!'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- CUSTOMER DETAILS ----------------
st.subheader("👤 Customer Details")

customer_name = st.text_input(
    "Customer Name",
    placeholder="Enter customer name",
    key="customer_name"
)


# ---------------- FOOD SELECTION ----------------
st.subheader("🍽️ Select Food Items")

selected_items = []

for index, (item, price) in enumerate(menu.items()):

    col1, col2, col3 = st.columns([3, 2, 2])

    # Food checkbox
    with col1:
        selected = st.checkbox(
            f"{item} — ₹{price}",
            key=f"food_checkbox_{index}"
        )

    # Quantity
    with col2:
        if selected:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=20,
                value=1,
                step=1,
                key=f"food_quantity_{index}"
            )
        else:
            quantity = 0

    # Item total
    with col3:
        item_total = price * quantity

        if selected:
            st.write(f"**₹{item_total:.2f}**")

    # Store selected item
    if selected:
        selected_items.append(
            (item, price, quantity, item_total)
        )


# ---------------- BILL SETTINGS ----------------
st.subheader("💰 Bill Settings")

col1, col2 = st.columns(2)

with col1:
    tax_rate = st.number_input(
        "GST / Tax (%)",
        min_value=0.0,
        max_value=30.0,
        value=5.0,
        step=0.5,
        key="tax_rate"
    )

with col2:
    discount_rate = st.number_input(
        "Discount (%)",
        min_value=0.0,
        max_value=50.0,
        value=0.0,
        step=1.0,
        key="discount_rate"
    )


# ---------------- GENERATE BILL ----------------
if st.button(
    "🧾 Generate Bill",
    use_container_width=True,
    key="generate_bill"
):

    if customer_name.strip() == "":
        st.warning("⚠️ Please enter the customer name.")

    elif not selected_items:
        st.warning("⚠️ Please select at least one food item.")

    else:

        # Calculate subtotal
        subtotal = sum(
            item[3] for item in selected_items
        )

        # Calculate discount
        discount_amount = (
            subtotal * discount_rate / 100
        )

        # Amount after discount
        amount_after_discount = (
            subtotal - discount_amount
        )

        # Calculate tax
        tax_amount = (
            amount_after_discount * tax_rate / 100
        )

        # Grand total
        grand_total = (
            amount_after_discount + tax_amount
        )


        # ---------------- BILL ----------------
        st.markdown("---")

        st.markdown(
            '<div class="bill-box">',
            unsafe_allow_html=True
        )

        st.markdown("## 🍔 KARISHMA RESTAURANT")

        st.write(
            f"**Customer:** {customer_name}"
        )

        st.write(
            f"**Date:** "
            f"{datetime.now().strftime('%d-%m-%Y %H:%M')}"
        )

        st.markdown("---")


        # ---------------- TABLE HEADER ----------------
        col1, col2, col3, col4 = st.columns(
            [4, 1, 2, 2]
        )

        with col1:
            st.write("**Item**")

        with col2:
            st.write("**Qty**")

        with col3:
            st.write("**Price**")

        with col4:
            st.write("**Total**")


        # ---------------- ITEMS ----------------
        for item, price, quantity, total in selected_items:

            col1, col2, col3, col4 = st.columns(
                [4, 1, 2, 2]
            )

            with col1:
                st.write(item)

            with col2:
                st.write(quantity)

            with col3:
                st.write(
                    f"₹{price:.2f}"
                )

            with col4:
                st.write(
                    f"₹{total:.2f}"
                )


        st.markdown("---")


        # ---------------- SUBTOTAL ----------------
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Subtotal**")

        with col2:
            st.write(
                f"**₹{subtotal:.2f}**"
            )


        # ---------------- DISCOUNT ----------------
        if discount_rate > 0:

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"Discount ({discount_rate:.1f}%)"
                )

            with col2:
                st.write(
                    f"- ₹{discount_amount:.2f}"
                )


        # ---------------- TAX ----------------
        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"GST / Tax ({tax_rate:.1f}%)"
            )

        with col2:
            st.write(
                f"₹{tax_amount:.2f}"
            )


        st.markdown("---")


        # ---------------- GRAND TOTAL ----------------
        st.markdown(
            f"""
            <div class="total">
                Grand Total: ₹{grand_total:.2f}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            '<div class="success">'
            '✅ Thank you for visiting!'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- FOOTER ----------------
st.markdown("---")

st.caption(
    "🍔 Karishma Restaurant Bill Generator "
    "| Built with Python + Streamlit"
)

