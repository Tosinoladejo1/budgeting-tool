from datetime import datetime
import calendar
import sqlite3


# Step 1: Choose currency
print("💵 Welcome to the Expense Tracker!")
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
   currency = input("Enter your custom currency symbol (e.g. ₹, ¥, ₩): ").strip()
else:
   print("⚠️ Invalid input. Defaulting to USD.")
   currency = "$"


# Step 2: Get income and budget
income = float(input(f"Enter your monthly income ({currency}): "))
monthly_budget = float(input(f"Enter your monthly budget ({currency}): "))


# Smart Allocation
today = datetime.today()
days_in_month = calendar.monthrange(today.year, today.month)[1]
default_daily_budget = monthly_budget / days_in_month
default_weekly_budget = monthly_budget / 4


print("\n💡 Smart Budget Suggestions:")
print(f"  Based on a monthly budget of {currency}{monthly_budget:.2f}:")
print(f"  ➤ Suggested weekly budget: {currency}{default_weekly_budget:.2f}")
print(f"  ➤ Suggested daily budget: {currency}{default_daily_budget:.2f}")


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


# Step 4: Categories and data
expenses = {
   "Groceries": [],
   "Transport": [],
   "Entertainment": [],
   "Rent": [],
   "Utilities": [],
   "Shopping": [],
   "Other": []
}


category_map = {
   "0": "Groceries",
   "1": "Transport",
   "2": "Entertainment",
   "3": "Rent",
   "4": "Utilities",
   "5": "Shopping",
   "6": "Other"
}


print("\n📥 Start entering your expenses. Type 'q' when you're done.\n")
while True:
   print("Select an expense category:")
   for key, value in category_map.items():
       print(f"{key} - {value}")
   category_input = input("Enter the category number or 'q' to quit: ").strip().lower()


   if category_input == "q":
       break
   if category_input not in category_map:
       print("❌ Invalid category. Try again.")
       continue


   category = category_map[category_input]
   try:
       amount = float(input(f"Enter the amount for {category} ({currency}): "))
   except ValueError:
       print("❌ Invalid amount. Try again.")
       continue


   if category == "Other":
       description = input("Add a short description for this 'Other' expense: ")
       expenses[category].append((amount, description))
   else:
       expenses[category].append(amount)


   print(f"✅ {category} expense of {currency}{amount:.2f} added.")


print("\n✅ All expenses recorded.")


# Budget check functions
def check_budget(expense, budget):
   if expense > budget:
       return f"⚠️ Over budget by {currency}{expense - budget:.2f}"
   elif expense < budget:
       return f"✅ Within budget by {currency}{budget - expense:.2f}"
   else:
       return "⚖️ Exactly on budget"


# Step 5: Calculate totals


remaining_income = income - total_expenses


# Final summary
print("\n🧾 Final Summary")
print(f"\n💰 Total Expenses: {currency}{total_expenses:.2f}")
print(f"💰 Remaining Income: {currency}{remaining_income:.2f}")
print(f"💰 Monthly Budget: {currency}{monthly_budget:.2f}")
print(f"💰 Weekly Budget: {currency}{weekly_budget:.2f}")
print(f"💰 Daily Budget: {currency}{daily_budget:.2f}")
print(f"{'⚠️ Over budget!' if total_expenses > monthly_budget else '✅ Within budget'}")


# Step 7: Category breakdown
print("\n📂 Expenses by Category:")
for cat, items in expenses.items():
   if cat == "Other":
       print(f"\n{cat}:")
       for amt, desc in items:
           print(f"  - {currency}{amt:.2f} → {desc}")
       print(f"  Total: {currency}{sum(item[0] for item in items):.2f}")
   else:
       print(f"  {cat}: {currency}{sum(items):.2f}")


# Step 8: Save to file
file_path = "expense_report.txt"
with open(file_path, "w") as f:
   f.write("💵 Expense Report\n")
   f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
   f.write(f"Monthly Income: {currency}{income:.2f}\n")
   f.write(f"Monthly Budget: {currency}{monthly_budget:.2f}\n")
   f.write(f"Total Expenses: {currency}{total_expenses:.2f}\n")
   f.write(f"Remaining Income: {currency}{remaining_income:.2f}\n\n")
   for cat, items in expenses.items():
       if cat == "Other":
           f.write(f"{cat}:\n")
           for amt, desc in items:
               f.write(f"  - {currency}{amt:.2f} → {desc}\n")
           f.write(f"  Total: {currency}{sum(item[0] for item in items):.2f}\n")
       else:
           f.write(f"{cat}: {currency}{sum(items):.2f}\n")


print(f"Report saved to {file_path}")


# Step 9: SQLite database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   category TEXT,
   amount REAL,
   description TEXT,
   date TEXT
)""")
conn.commit()


for category, amounts in expenses.items():
   if category == "Other":
       for amount, description in amounts:
           cursor.execute("INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)",
                          (category, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
   else:
       for amount in amounts:
           cursor.execute("INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)",
                          (category, amount, None, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
conn.commit()


cursor.execute("SELECT * FROM expenses")
rows = cursor.fetchall()
for row in rows:
   print(row)
conn.close()


# Step 10: Summary from DB
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
rows = cursor.fetchall()
print("\n🧾 Summary Report from Database")
for row in rows:
   print(f"{row[0]}: {currency}{row[1]:.2f}")
conn.close()


# Step 11: User feedback
print("\n📝 User Feedback")
feedback = input("Please provide your feedback on this expense tracker: ")
with open("user_feedback.txt", "a") as f:
   f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {feedback}\n")


print("Thank you for your feedback!")


# Step 12: End of program
print("\n🎉 Thank you for using the Expense Tracker!")
# You can find your report in the same directory as this script.
# You can also find your feedback in user_feedback.txt
# and your expenses in the expenses.db database.
# Have a great day!
# Close the database connection
