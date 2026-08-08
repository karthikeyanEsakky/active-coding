def game(level,stats):
    if level >=2:
        print("you are a pro",level)
    else:
        print("you can do it",level)
    
    print("You have "+stats)
    return "play well"

a=game(3,"100 kills")
b=game(1,"20 kills")
print(a)
print(b) 