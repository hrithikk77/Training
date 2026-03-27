# 1. remove duplicates while preserving the order


# nums = [1, 2, 2, 3, 4, 4, 5]
# num2 =[]
# for i in  nums:
#     if i in num2:
#         pass
#     else:
#         num2.append(i)

# print(num2)



# 2.  Second Largest Unique Element

# nums = [10, 20, 4, 45, 55 ,99, 99]
# num2 =[]
# for i in  nums:
#     if i in num2:
#         pass
#     else:
#         num2.append(i)
# num2.sort()
# print(num2[len(num2)-2])




# 3.  Group Anagrams 

# Problem Statement: 
# Group strings that are anagrams of each other. 

# Input: 
# words = ["eat","tea","tan","ate","nat","bat"] 

# Output: 
# [["eat","tea","ate"],["tan","nat"],["bat"]] 

# Ans 

# def groupAnagrams(words):
#     result = {}   

#     for word in words:
        
#         sorted_word = ''.join(sorted(word))

#         # Step 2: check if key exists
#         if sorted_word in result:
#             result[sorted_word].append(word)
#         else:
#             result[sorted_word] = [word]
#             print(result)

#     # Step 3: return grouped values
#     return list(result.values())


# words = ["eat","tea","tan","ate","nat","bat"]
# print(groupAnagrams(words))








# 4.Top K Frequent Elements 

# Problem Statement: 
# Return the k most frequent elements. 

# Input: 
# nums = [1,1,1,2,2,3], k = 2 

# Output: 
# [1,2] 

# def top_k_frequent(nums,k): 
#     freq ={} 
#     for num in nums: 
#         freq[num]=freq.get(num,0)+1 
#     buckets=[[]for _ in range(len(nums)+1)] 
#     for num,count in freq.items(): 
#         buckets[count].append(num) 
#     result=[] 
#     for i in range(len(buckets)-1,0,-1): 

#         for num in buckets[i]: 

#             result.append(num) 

#             if len(result)==k: 

#                 return result    

# nums=[1,1,1,2,2,3,] 
# k=2 
# print(top_k_frequent(nums,k)) 





# 5. Word Frequency Counter (File Handling) 

# Problem Statement: 
# Read a .txt file and count frequency of each word. 

# Input (file content): 

# hello world 
# hello python 

# Output: 
# {'hello':2,'world':1,'python':1} 



# import string  

# def word_frequency(file_path): 
#     freq={} 
#     with open(r"C:\\Users\\hrithik.k\\Desktop\\python\\test.txt",'r') as file: 

#         for line in file: 

#             line=line.lower() 

#             line=line.translate(str.maketrans('','',string.punctuation)) 

#             words=line.split() 

 

#             for word in words: 

#                 if word in freq: 

#                     freq[word]+=1 

#                 else: 

#                     freq[word]=1 

#     return freq 

# print(word_frequency("text1.txt")) 







#6. JSON Validation 
# Problem Statement: 
# Check if a string is a valid JSON. 

# Input: 
# '{"name": "John", "age": 30}' 

# Output: 
# True 



#7. import json 

# def is_valid_json(json_string): 

#     try: 

#         json.loads(json_string) 

#         return True 

#     except json.JSONDecodeError: 

#         return False 

# print(is_valid_json('{"name":"john","age":30}')) 

# print(is_valid_json('{"name":"Hrithik","age":}')) 





#8. Custom Exception Handling 

# Problem Statement: 
# Raise a custom exception if salary < 10000. 

# Input: 
# salary = 8000 

# Output: 
# "SalaryTooLowError" 


#define custom exception 

# class SalaryTOOLOWError(Exception): 
#     pass 
# def check_Salary(salary): 
#     if salary <10000: 
#         raise SalaryTOOLOWError("Salary too low") 
#     return "salary accepted" 
# salary1=8000 
# try: 
#     print(check_Salary(salary1)) 
# except SalaryTOOLOWError as e: 
#     print(e) 




#9.  Flatten Nested List (Recursive) 

# Problem Statement: 
# Flatten a nested list of arbitrary depth. 

# Input: 
# [1,[2,[3,4],5],6] 

# Output: 
# [1,2,3,4,5,6] 

# def flatten_list(nested_list): 
#     result=[] 
#     for item in nested_list: 
#         if isinstance(item,list): 
#             result.extend(flatten_list(item)) 
#         else: 
#             result.append(item) 
#     return result 

# data=[1,[2,[3,4],5],6] 
# print(flatten_list(data)) 




#10. Lambda + Sorting Complex Structure 

# Problem Statement: 
# Sort list of dictionaries by age. 

# Input: 
# [{'name':'A','age':30},{'name':'B','age':20}] 

# Output: 
# [{'name':'B','age':20},{'name':'A','age':30}] 


# data=[{'name':'A','age':30},{'name':'B','age':20}]
# sorted_data=sorted(data,key=lambda x:x['age']) 

# print(sorted_data) 





#11.  Environment Variables Loader 

# Problem Statement: 
# Read variables from .env file and load into program. 

# Input (.env): 

# DB_HOST=localhost 
# DB_PORT=5432 

# Output: 
# {'DB_HOST':'localhost','DB_PORT':'5432'} 

# def load_env(file_path): 
#     env_vars = {} 
#     with open(r".env", 'r') as file: 
#         for line in file: 
#             line = line.strip() 
#             # Skip empty lines or comments 
#             if not line or line.startswith('#'): 
#                 continue 
#             # Split key and value 
#             key, value = line.split('=', 1) 
#             env_vars[key.strip()] = value.strip() 
#     return env_vars 

# # Example 
# env = load_env(".env") 

# print(load_env(env))






# --------------------------------------
#12. Logging System 

# Problem Statement: 
# Log errors with timestamp to file (txt or Json). 

# Output Format: 

# 2026-01-01 10:00:00 ERROR Something failed

# import logging 
# # Configure logging 
# logging.basicConfig( 
#     filename='app.log',              # file name 
#     level=logging.ERROR,             # log only errors 
#     format='%(asctime)s %(levelname)s %(message)s', 
#     datefmt='%Y-%m-%d %H:%M:%S' 
# ) 
# # Example function 
# def divide(a, b): 
#     try: 
#         return a / b 
#     except Exception as e: 
#         logging.error("Something failed: %s", str(e)) 
# # Trigger error 
# print(divide(10, 89)) 








#13. Create Dictionary from Two Lists 

# Problem Statement: 
# Given two lists, create a dictionary mapping keys to values. 
# Input: 
# keys = ['a','b','c'] 
# values = [1,2,3] 
# Output: 
# {'a':1,'b':2,'c':3} 


# keys=['a','b','c'] 
# values=[1,2,3] 
# result={k: v for k, v in zip(keys,values)} 
# print(result) 




#14. Invert Dictionary Using Comprehension 
# Input: 
# {'a':1,'b':2,'c':3} 
# Output: 
# {1:'a',2:'b',3:'c'} 


# data={'a':1,'b':2,'c':3} 

# inverted={v:k for k, v in data.items()} 

# print(inverted) 



#15. Extract Words Starting with Vowel 

# Input: 
# "apple banana orange grape" 

# Output: 
# ["apple","orange"] 


# text = "apple banana orange grape" 
# result = [word for word in text.split() if word[0].lower() in 'aeiou'] 
# print(result) 



#16. Replace Negative Numbers with 0 

# Input: 
# [1,-2,3,-4,5] 

# Output: 
# [1,0,3,0,5] 

# nums=[1,-2,3,-4,5] 
# result=[x if x >=0 else 0 for x in nums] 
# print(result) 

#17. Multi-condition List Comprehension 
# Problem Statement: 
# Return numbers divisible by both 2 and 3. 

# Input: 
# range(1,20) 

# Output: 
# [6,12,18] 

# result=[x for x in range(1,20)if x %2==0 and x %3 ==0] 
# print(result) 



#18. Smart Banking System (OOP + SRP + Encapsulation) 
# Problem 
# Design a banking system with: 
# Deposit 
# Withdraw 
# Balance check 

# class TransactionLogger: 
#     def log(self, message): 
#         print(f"[LOG]: {message}") 

# class Account: 
#     def __init__(self, name, balance): 
#         self.name = name 
#         self.__balance = balance   # private variable 
#         self.logger = TransactionLogger() 

#     def deposit(self, amount): 
#         if amount <= 0: 
#             raise ValueError("Invalid deposit amount") 
#         self.__balance += amount 
#         self.logger.log(f"{amount} deposited") 

#     def withdraw(self, amount): 
#         if amount <= 0: 
#             raise ValueError("Invalid withdraw amount") 
#         if amount > self.__balance: 
#             raise ValueError("Insufficient balance")
#         self.__balance -= amount 
#         self.logger.log(f"{amount} withdrawn") 
#     def get_balance(self): 
#         return f"Balance: {self.__balance}" 

# # Usage 
# acc = Account("John", 1000) 
# acc.deposit(500) 
# acc.withdraw(200) 
# print(acc.get_balance()) 






 

# Bird System Fix (LSP + Inheritance Design) 
# Problem 
# Fix this design: 
# class Bird: 
#    def fly(self): 
#        pass 
# class Penguin(Bird): 
#    def fly(self): 
#        raise Exception("Cannot fly") 

# Task 
# Redesign system so: 
# No subclass breaks behavior 
# LSP is followed 
# Expected Output 
# Sparrow flies 
# Penguin swims 

# class Bird: 
#     pass 
# class Flyable: 
#     def fly(self): 
#         pass 
# class Swimmable: 
#     def swim(self): 
#         pass 
# class Sparrow(Bird, Flyable): 
#     def fly(self): 
#         print("Sparrow flies") 

# class Penguin(Bird, Swimmable): 
#     def swim(self): 
#         print("Penguin swims") 
# # Usage 
# sparrow = Sparrow() 
# penguin = Penguin() 
# sparrow.fly() 
# penguin.swim() 






#19. E-Commerce Checkout System (ALL SOLID + OOP) 

# Problem 
# Design checkout system with: 
# Multiple payment methods (UPI, Card) 
# Discount system (Festival, Premium user) 
# Logging 


# class Payment: 
#     def pay(self, amount): 
#         pass 

# class UPI(Payment): 
#     def pay(self, amount): 
#         print("Payment Successful via UPI") 

# class Card(Payment): 
#     def pay(self, amount): 
#         print("Payment Successful via Card") 

# class Discount: 
#     def apply(self, amount): 
#         return amount 

# class FestivalDiscount(Discount): 
#     def apply(self, amount): 
#         return amount * 0.9   # 10% discount  

# class PremiumDiscount(Discount): 
#     def apply(self, amount): 
#         return amount * 0.8   # 20% discount 

# class Logger: 
#     def log(self, message): 
#         print(f"[LOG]: {message}") 

# class Checkout: 

#     def __init__(self, payment: Payment, discount: Discount): 
#         self.payment = payment 
#         self.discount = discount 
#         self.logger = Logger() 
    
#     def process(self, amount): 
#         final_amount = self.discount.apply(amount) 
#         print(f"Final Amount: {int(final_amount)}") 
#         self.payment.pay(final_amount) 
#         self.logger.log("Checkout completed") 

# checkout = Checkout(payment=UPI(), discount=FestivalDiscount()) 
# checkout.process(1000) 





