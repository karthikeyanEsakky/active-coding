students = {}

while True:
    print("\n1. Add")
    print("2. View")
    print("3. Search")
    print("4. Update")
    print("5. Delete")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        usn = input("Enter ID: ")
        name = input("Enter Name: ")
        course = input("Enter Course: ")
        age = input("Enter Age: ")

        students[usn] = {
            "Name": name,
            "Course": course,
            "Age": age
        }

    elif choice == "2":
        print("\nStudent Records")
        for usn, details in students.items():
            print("ID:", usn)
            print("Name:", details["Name"])
            print("Course:", details["Course"])
            print("Age:", details["Age"])
            print()

    elif choice == "3":
        usn = input("Enter ID: ")
        if usn in students:
            print("Name:", students[usn]["Name"])
            print("Course:", students[usn]["Course"])
            print("Age:", students[usn]["Age"])
        else:
            print("Student not found")

    elif choice == "4":
        usn = input("Enter ID: ")
        if usn in students:
            students[usn]["Name"] = input("Enter New Name: ")
            students[usn]["Course"] = input("Enter New Course: ")
            students[usn]["Age"] = input("Enter New Age: ")
            print("Updated")
        else:
            print("Student not found")

    elif choice == "5":
        usn = input("Enter ID: ")
        if usn in students:
            del students[usn]
            print("Deleted")
        else:
            print("Student not found")

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")