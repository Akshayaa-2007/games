import random
print("Welcome to the number guessing game")
print("I am thinking of number between 1 and 10")
while True:
 n=random.randrange(1,10)
 user_guess=int(input("Enter your guessing number:"))
 if user_guess==n:
     print("Right")
     break
 elif user_guess>=n:
     print("too high")
 elif user_guess<=n:
     print("too low")
 else:
        print("invallid input")