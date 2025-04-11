from datetime import datetime, timedelta
import calendar

# Step 1: Get Monthly Income and Budget
print("💰 Welcome to the Budget Tracker!")
try:
    income = float(input("Enter your monthly income: "))
    monthly_budget = float(input("Enter your monthly budget: "))
except ValueError:
    print("⚠️ Invalid input. Please enter numeric values.")
    exit()
# Check if monthly budget exceeds income
if monthly_budget > income:
    print("❌ Monthly budget cannot exceed monthly income.")
    exit()
# Step 1.1: Currency Selection
print("💵 Choose your currency:")
print("1 - USD ($)")
print("2 - EUR (€)")
print("3 - GBP (£)")
print("4 - CAD (C$)")
print("5 - NGN (₦)")
print("6 - Type your own symbol")

currency_input = input("Enter your choice (1–6): ").strip()

currency_symbols = {
    "1": "$",
    "2": "€",
    "3": "£",
    "4": "C$",
    "5": "₦"
}

if currency_input in currency_symbols:
    currency = currency_symbols[currency_input]
elif currency_input == "6":
    currency = input("Type your custom currency symbol (e.g. ₹, ¥, ₫, ₴): ").strip()
else:
    print("Invalid input. Defaulting to USD ($)")
    currency = "$"
print(f"Selected currency: {currency}")
# Step 2: Smart Allocation
today = datetime.today()
days_in_month = calendar.monthrange(today.year, today.month)[1]

default_daily_budget = monthly_budget / days_in_month
default_weekly_budget = monthly_budget / 4

print("\n💡 Budget Suggestions:")
print(f"  Based on a monthly budget of {monthly_budget:.2f}:")
print(f"  ➤ weekly budget: {default_weekly_budget:.2f}")
print(f"  ➤ daily budget: {default_daily_budget:.2f}")

# Step 3: Ask if user wants to override
use_custom = input("\nDo you want to set custom daily or weekly budgets? (yes/no): ").strip().lower()

if use_custom == 'yes':
    try:
        weekly_budget = float(input("Enter your custom weekly budget: "))
        daily_budget = float(input("Enter your custom daily budget: "))
    except ValueError:
        print("⚠️ Invalid input. Falling back to smart suggestions.")
        weekly_budget = default_weekly_budget
        daily_budget = default_daily_budget
else:
    weekly_budget = default_weekly_budget
    daily_budget = default_daily_budget

# Step 4: Set up categories and logs
category_map = {
    "0": "Groceries",
    "1": "Transport",
    "2": "Entertainment",
    "3": "Rent",
    "4": "Utilities",
    "5": "Shopping",
    "6": "Other"
}

expenses = {cat: [] for cat in category_map.values()}
expense_log = []

print("\n📥 Start entering your expenses. Type 'done' to finish.\n")

# Step 5: Batch input loop
while True:
    print("Select an expense category:")
    for key, value in category_map.items():
        print(f"{key} - {value}")
    category_input = input("Enter the category number or 'done' to finish: ").strip().lower()

    if category_input == 'done':
        break

    if category_input not in category_map:
        print("❌ Invalid category. Try again.")
        continue

    category_name = category_map[category_input]

    try:
        amount = float(input(f"Enter amount for {category_name}: "))
    except ValueError:
        print("❌ Please enter a valid number.")
        continue
    
    if category_name == "Other":
        note = input("Add a short description for this 'Other' expense: ")
    else:
        note = ""

    expenses[category_name].append(amount)
    expense_log.append({
        "amount": amount,
        "category": category_name,
        "timestamp": datetime.now()
    })

print("\n✅ All expenses recorded.")

# Step 6: Budget check functions
def get_total_spent_in_period(days: int):
    now = datetime.now()
    start = now - timedelta(days=days)
    return sum(e['amount'] for e in expense_log if e['timestamp'] >= start)

total_spent = sum(e['amount'] for e in expense_log)
daily_spent = get_total_spent_in_period(1)
weekly_spent = get_total_spent_in_period(7)
remaining_income = income - total_spent

# Step 7: Final Summary
print("\n🧾 Final Summary")
print(f"Total Expenses: ${total_spent:.2f}")
print(f"Remaining Income: ${remaining_income:.2f}")

print("\n📊 Budget Breakdown:")
print(f"  Daily Limit:   {daily_budget:.2f} | Spent: {daily_spent:.2f} → {'⚠️ Over Budget!' if daily_spent > daily_budget else '✅ OK'}")
print(f"  Weekly Limit:  {weekly_budget:.2f} | Spent: {weekly_spent:.2f} → {'⚠️ Over Budget!' if weekly_spent > weekly_budget else '✅ OK'}")
print(f"  Monthly Limit: {monthly_budget:.2f} | Spent: {total_spent:.2f} → {'⚠️ Over Budget!' if total_spent > monthly_budget else '✅ OK'}")

print("\n📂 Expenses by Category:")
for cat, amounts in expenses.items():
    print(f"  {cat}: {sum(amounts):.2f}")
print("\n📋 Detailed Expense Log:")
for entry in expense_log:
    if entry['category'] == "Other":
        time_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M")
        print(f"  - ${entry['amount']:.2f} on {time_str} → {entry['description']}")
    print(f"  {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {entry['category']}: ${entry['amount']:.2f}")
print("\n💡 Tips for Budgeting:")
print("  - Review your expenses weekly.")
print("  - Adjust your budget based on spending patterns.")
print("  - Use cash for discretionary spending.")


# Step 8: Save to file (optional)
with open("expense_log.txt", "w") as f:
    for entry in expense_log:
        f.write(f"{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} - {entry['category']}: ${entry['amount']:.2f}\n")
print("📂 Expense log saved to 'expense_log.txt'.")
# Step 9: End of program
print("\n👋 Thank you for using the Smart Budget Tracker!")
# This is a simple budget tracker that helps you manage your expenses and stay within your budget. It allows you to set a monthly budget, track your expenses by category, and provides suggestions for daily and weekly budgets based on your monthly budget. The program also includes features for batch input of expenses, budget checks, and a detailed expense log.
