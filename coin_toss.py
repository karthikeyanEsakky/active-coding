import random
coin=random.randint(0,1)
computer_choice=random.randint(0,1)
print("Available choices are Heads and Tails, Begin!!")
rev_dic={0:"Heads",1:"Tails"}
str_conv=rev_dic[computer_choice]
coin_choice=rev_dic[coin]

my_choice = input("Enter your choice :")

if my_choice not in ["Heads", "Tails"]:
    print("Invalid Input")
    converted_choice=None
    
else:
    dic = {"Heads":0, "Tails":1}
    converted_choice = dic[my_choice]
    print(f"The computer Chose : {str_conv}")
    print(f"The coin flipped to {coin_choice}")
    if converted_choice==computer_choice:
          print("It's a Draw")
    
    else:
        if converted_choice==coin:
            print("You Won")
        elif computer_choice==coin:
                print("You Lose")
   
print("Thanks for Playing")
    



