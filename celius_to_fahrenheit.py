def cel_to_fah(cel):
    fah=(cel*9/5)+32
    return fah

cel=int(input("Enter the temperature in celsuis:"))
conv=cel_to_fah(cel)
print(f"The temperature in fahrenheit is {conv:.2f}°F")
