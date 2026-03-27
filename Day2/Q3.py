# Q3. Composition — Order with Address and Payment 
# Topics: Composition, SRP 
# Problem Statement: 
# Build an Order class using composition. Create separate classes: Address (city, zip_code), PaymentInfo (method, amount), and OrderItem (name, qty, price). The Order class should contain an Address, PaymentInfo, and a list of OrderItems. Implement order_summary() that returns the full breakdown. 
# Input: 
# addr = Address("Bangalore", "560001") 
# pay = PaymentInfo("UPI", 1500) 
# items = [OrderItem("Book", 2, 500), OrderItem("Pen", 5, 100)] 
# order = Order(addr, pay, items) 
# order.order_summary()
# Output: 
# Shipping: Bangalore - 560001 
# Items: Book x2 = 1000, Pen x5 = 500 
# Total: 1500 
# Payment: UPI 
# Constraints: 
# Do NOT use inheritance; use composition only 
# Each class must have a single responsibility 
# OrderItem total = qty * price 

 











class Address:
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code


class PaymentInfo:
    def __init__(self, method, amount):
        self.method = method
        self.amount = amount


class OrderItem:
    def __init__(self, name, qty, price):
        self.name = name
        self.qty = qty
        self.price = price

    def total(self):
        return self.qty * self.price


class Order:
    def __init__(self, address, payment, items):
        self.address = address          
        self.payment = payment          
        self.items = items              

    def order_summary(self):
        
        print(f"Shipping: {self.address.city} - {self.address.zip_code}")

        
        item_strings = []
        total_amount = 0

        for item in self.items:
            item_total = item.total()
            total_amount += item_total
            item_strings.append(f"{item.name} x{item.qty} = {item_total}")

        print("Items: " + ", ".join(item_strings))

        
        print(f"Total: {total_amount}")

        print(f"Payment: {self.payment.method}")



addr = Address("Bangalore", "560001")
pay = PaymentInfo("UPI", 1500)

items = [
    OrderItem("Book", 2, 500),
    OrderItem("Pen", 5, 100)
]

order = Order(addr, pay, items)
order.order_summary()