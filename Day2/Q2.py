# Q2. Inheritance — Admin and Customer Users 
# Topics: Inheritance, Polymorphism, super() 
# Problem Statement: 
# Create a base class User with attributes username and role, and a method display_profile(). Create two subclasses: AdminUser (extra attribute: permissions list) and CustomerUser (extra attribute: orders count). Override display_profile() in both subclasses to include their specific data. 

# Input: 
# admin = AdminUser("admin1", ["manage_users", "view_logs"]) 
# customer = CustomerUser("cust1", 5) 
# admin.display_profile() 
# customer.display_profile() 
# Output: 
# Admin: admin1 | Permissions: manage_users, view_logs 
# Customer: cust1 | Orders: 5 
# Constraints: 
# Use super().__init__() to initialize base class 
# Override display_profile() in each subclass (Polymorphism) 
# Permissions must be a list of strings 

 






class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def display_profile(self):
        print(f"User: {self.username} | Role: {self.role}")


class AdminUser(User):
    def __init__(self, username, permissions):
        super().__init__(username, "Admin")   
        
        if not isinstance(permissions, list) or not all(isinstance(p, str) for p in permissions):
            raise ValueError("Permissions must be a list of strings")
        
        self.permissions = permissions

    def display_profile(self):  
        perms = ", ".join(self.permissions)
        print(f"Admin: {self.username} | Permissions: {perms}")


class CustomerUser(User):
    def __init__(self, username, orders_count):
        super().__init__(username, "Customer")  
        self.orders_count = orders_count

    def display_profile(self):  # method overriding
        print(f"Customer: {self.username} | Orders: {self.orders_count}")




admin = AdminUser("admin1", ["manage_users", "view_logs"])
customer = CustomerUser("cust1", 5)

admin.display_profile()
customer.display_profile()