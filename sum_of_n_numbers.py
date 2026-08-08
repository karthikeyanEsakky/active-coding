def sum(n):
    if n==0:
        return 0
    else:
        return n + sum(n-1)
n=int(input("Eneter the value:"))
sum=sum(n)
print(f"The total sum of n numbers is {sum}")