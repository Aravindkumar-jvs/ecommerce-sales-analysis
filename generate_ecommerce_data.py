import csv
import random
from datetime import date, timedelta

random.seed(99)

categories = ["Electronics", "Clothing", "Home & Kitchen", "Sports", "Books", "Beauty", "Toys", "Automotive"]
cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]
payment_methods = ["Credit Card", "Debit Card", "UPI", "Net Banking", "COD", "Wallet"]
statuses = ["Delivered", "Returned", "Cancelled", "Pending"]
status_weights = [70, 10, 12, 8]

products = {
    "Electronics": [("Smartphone", 15000, 45000), ("Laptop", 35000, 90000), ("Earphones", 800, 5000), ("Smartwatch", 3000, 20000)],
    "Clothing": [("T-Shirt", 300, 1200), ("Jeans", 800, 3000), ("Dress", 600, 4000), ("Jacket", 1200, 6000)],
    "Home & Kitchen": [("Mixer", 1500, 5000), ("Cookware Set", 800, 4000), ("Air Purifier", 5000, 15000), ("Bedsheet", 400, 2000)],
    "Sports": [("Cricket Bat", 800, 5000), ("Yoga Mat", 400, 1500), ("Dumbbells", 600, 3000), ("Running Shoes", 1500, 6000)],
    "Books": [("Fiction Novel", 200, 600), ("Self Help", 150, 500), ("Textbook", 300, 1200), ("Comic", 100, 400)],
    "Beauty": [("Moisturizer", 200, 1500), ("Serum", 400, 3000), ("Lipstick", 150, 800), ("Perfume", 500, 5000)],
    "Toys": [("LEGO Set", 800, 4000), ("Board Game", 400, 2000), ("RC Car", 600, 3000), ("Doll", 300, 1500)],
    "Automotive": [("Car Covers", 500, 2000), ("Seat Cushion", 400, 1500), ("Dash Cam", 2000, 8000), ("Tyre Inflator", 800, 3000)],
}

def random_date(start_year=2022, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

customers = [f"CUST{str(i).zfill(4)}" for i in range(1, 201)]
customer_city = {c: random.choice(cities) for c in customers}

orders = []
for i in range(1, 501):
    cat = random.choice(categories)
    prod_name, min_price, max_price = random.choice(products[cat])
    price = round(random.uniform(min_price, max_price), 2)
    qty = random.randint(1, 4)
    discount = round(random.uniform(0, 0.30), 2)
    revenue = round(price * qty * (1 - discount), 2)
    order_date = random_date()
    customer = random.choice(customers)
    status = random.choices(statuses, weights=status_weights)[0]
    payment = random.choice(payment_methods)
    rating = round(random.uniform(2.5, 5.0), 1) if status == "Delivered" else None

    orders.append({
        "Order_ID": f"ORD-{10000+i}",
        "Customer_ID": customer,
        "City": customer_city[customer],
        "Category": cat,
        "Product_Name": prod_name,
        "Unit_Price": price,
        "Quantity": qty,
        "Discount_Pct": discount,
        "Revenue": revenue,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Year": order_date.year,
        "Month": order_date.month,
        "Quarter": f"Q{(order_date.month-1)//3+1}",
        "Payment_Method": payment,
        "Order_Status": status,
        "Customer_Rating": rating if rating else ""
    })

with open("ecommerce_orders.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=orders[0].keys())
    writer.writeheader()
    writer.writerows(orders)

print(f"Generated {len(orders)} orders → ecommerce_orders.csv")
