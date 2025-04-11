# income = float(input("Enter your monthly expenses: "))

total_income = 0
expenses ={"Groceries": [],
    "Transport": [],
    "Entertainment": [], "Rent": [], "Utilities": [],"shopping": [],
    "Other": []}

# Ask for monthly income before calulating expenses
income = float(input("Enter your monthly income: "))

while True:
    # Allow the user pick the expense category, with labeled options (e.g 0 - Shopping, etc)
    print("Select an expense category")
    print("0 - Groceries")
    print("1 - Transport")
    print("2 - Entertainment")
    print("3 - Rent")
    print("4 - Utilities")
    print("5 - Shopping")
    print("6 - Other")
    print("Enter the number of the category or enter q to quit:", end=" ")
    category_description = None
    category = input()
    if category == "q":
        break
    category = int(category)
    if category == 0:
        category_description = "Groceries"
    elif category == 1:
        category_description = "Transport"
    elif category == 2:
        category_description = "Entertainment"
    elif category == 3:
        category_description = "Rent"
    elif category == 4:
        category_description = "Utilities"
    elif category == 5:
        category_description = "Shopping"
    elif category == 6:
        category_description = "Other"
    else:
        print("Invalid category. Please enter a valid category.")
        continue
    
    # this is just an extra check to make sure the user is entering a valid expense category
    if category_description not in expenses:
        print("Invalid expense category. Please enter a valid category.")
        continue
    amount = float(input("Enter the amount: "))
   
    total_income += amount
    if category_description in expenses:
        expenses[category_description].append(amount)
    else:
        expenses["Other"].append(amount)
        
        
# Calculate what is left after deducting expenses from the income given at the start
total_expenses = sum([sum(expense) for expense in expenses.values()])
remaining_income = income - total_expenses
print("Total expenses:", total_expenses)
print("Remaining income:", remaining_income)
print("Expenses by category:")
for category, amounts in expenses.items():
    print(f"{category}: {sum(amounts)}")