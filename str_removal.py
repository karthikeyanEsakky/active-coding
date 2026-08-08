def rem(l,word):
    for item in l:
        l.remove(word)
        return l


l=["karthik","name","game"]
print(l)
rem(l,"karthik")
print(l)