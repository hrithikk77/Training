# Q6. LSP — Fix the Bird Hierarchy 
# Topics: LSP, ISP, Abstraction 
# Problem Statement: 
# The following design violates LSP: 
# class Bird: def fly(self): ... 
# class Penguin(Bird): def fly(self): raise Exception("Can't fly") 
# Redesign the hierarchy so that no subclass breaks the contract of its parent. Create proper abstract classes: Bird, FlyingBird, SwimmingBird. Implement Sparrow, Eagle, Penguin, and Duck (Duck both flies and swims). 
# Input: 
# for bird in [Sparrow(), Eagle(), Penguin(), Duck()]: 
#     bird.move() 

# Output: 
# Sparrow flies 
# Eagle flies 
# Penguin swims 
# Duck flies and swims 

# Constraints: 
# No method should raise an unexpected exception 
# Use abstract base classes with ABC 
# Duck must implement both flying and swimming interfaces 
# LSP: every subclass must be substitutable for its parent 

 


from abc import ABC, abstractmethod

# 1 Base abstract class
class Bird(ABC):
    @abstractmethod
    def move(self):
        pass

# 2 Flying capability
class FlyingBird(Bird):
    @abstractmethod
    def fly(self):
        pass

# 3 Swimming capability
class SwimmingBird(Bird):
    @abstractmethod
    def swim(self):
        pass


# 4 Concrete classes
class Sparrow(FlyingBird):
    def fly(self):
        return "Sparrow flies"

    def move(self):
        return self.fly()


class Eagle(FlyingBird):
    def fly(self):
        return "Eagle flies"

    def move(self):
        return self.fly()


class Penguin(SwimmingBird):
    def swim(self):
        return "Penguin swims"

    def move(self):
        return self.swim()


class Duck(FlyingBird, SwimmingBird):
    def fly(self):
        return "Duck flies"

    def swim(self):
        return "Duck swims"

    def move(self):
        return f"{self.fly()} and {self.swim()}"
    



for bird in [Sparrow(), Eagle(), Penguin(), Duck()]:
    print(bird.move())




# hrithik@K77