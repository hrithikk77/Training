# Q5. OCP — Extensible Discount System 
# Topics: OCP, Abstraction 
# Problem Statement: 
# Create a discount system where new discount types can be added without modifying existing code. Define an abstract base class Discount with method apply(amount). Implement: NoDiscount, PercentageDiscount (10%), FlatDiscount (Rs 200 off), and BuyOneGetOneFree (50% off). Write a function calculate_total(amount, discount). 

# Input: 
# print(calculate_total(1000, PercentageDiscount())) 
# print(calculate_total(1000, FlatDiscount())) 
# print(calculate_total(1000, BuyOneGetOneFree())) 

# Output: 
# 900.0 
# 800.0 
# 500.0 

# Constraints: 
# Use ABC and @abstractmethod 
# Adding a new discount type must NOT modify calculate_total() 
# Discount cannot return negative amounts; minimum is 0 

 







from abc import ABC, abstractmethod

# 1 Abstract Base Class
class Discount(ABC):
    @abstractmethod
    def apply(self, amount):
        pass

# 2 Concrete Discount Classes
class NoDiscount(Discount):
    def apply(self, amount):
        return amount

class PercentageDiscount(Discount):
    def apply(self, amount):
        return max(0, amount * 0.9)   # 10% off

class FlatDiscount(Discount):
    def apply(self, amount):
        return max(0, amount - 200)

class BuyOneGetOneFree(Discount):
    def apply(self, amount):
        return max(0, amount * 0.5)

# 3 Function (Closed for modification)
def calculate_total(amount, discount: Discount):
    return discount.apply(amount)

print(calculate_total(1000, PercentageDiscount()))
print(calculate_total(1000, FlatDiscount()))
print(calculate_total(1000, BuyOneGetOneFree()))