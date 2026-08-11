import random
random_number=random.choice([1,-1,0])
print("You choice can be Snake,Water,Gun")
my_choice=input("Enter your choice :")
dict={"Gun":1,"Water":0,"Snake":-1}
revdict={1:"Gun",0:"Water",-1:"Snake"}
conv=dict[my_choice]
computer_choice=revdict[random_number]
print(f"Your chose is {my_choice}")
print(f"The computer chose {computer_choice}")
if conv==random_number:
    print("draw")
else:
    if (conv==1 and random_number==-1):
        print("You win")
    elif (conv==-1 and random_number==0):
            print("You win")
    elif (conv==0 and random_number==1):
            print("You win")
    elif (conv==0 and random_number==-1):
            print("You lose")
    elif (conv==-1 and random_number==1):
            print("You lose")
    elif (conv==1 and random_number==0):
            print("You lose")
    else:
        print("Invalid Input")
print("Thank You for playing")
    

