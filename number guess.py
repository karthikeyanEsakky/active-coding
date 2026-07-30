import random

number = random.randint(1, 100)
attempts = 0

while True:
    guess = int(input("Enter your guess (1-100): "))
    attempts += 1

    if guess < number:
        print("Too Low!")

    elif guess > number:
        print("Too High!")

    else:
        print("Congratulations! You guessed it.")
        print("Attempts:", attempts)
        break