from datetime import datetime, timedelta
import calendar
import sqlite3

# ------------------------- Utility Functions -------------------------

def get_currency():
    print("💵 Choose your currency:")
    print("1 - USD ($)\n2 - EUR (€)\n3 - GBP (£)\n4 - CAD (C$)\n5 - NGN (₦)\n6 - Type your own symbol")
    currency_symbols = {"1": "$", "2": "€", "3": "£", "4": "C$", "5": "₦"}
    choice = input("Enter your choice (1–6): ").strip()
    return currency_symbols.get(choice, input("Enter your custom currency symbol (e.g. ₹, ¥, ₩): ").strip() if choice == "6" else "$")


def calculate_budgets(monthly_budget):
    today = datetime.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    return monthly_budget / days_in_month, monthly_budget / 4


def get_income_and_budget(currency):
    try:
        income = float(input(f"Enter your monthly income ({currency}): "))
        budget = float(input(f"Enter your monthly budget ({currency}): "))
        return income, budget
    except ValueError:
        print("⚠️ Invalid input. Please enter numeric values.")
        exit()


def get_custom_budgets(default_daily, default_weekly):
    use_custom = input("Do you want to set custom daily or weekly budgets? (yes/no): ").strip().lower()
    if use_custom == 'yes':
        try:
            weekly = float(input("Enter your custom weekly budget: "))
            daily = float(input("Enter your custom daily budget: "))
            return daily, weekly
        except ValueError:
            print("⚠️ Invalid input. Falling back to smart suggestions.")
    return default_daily, default_weekly


def input_expenses(currency):
    category_map = {
        "0": "Groceries", "1": "Transport", "2": "Entertainment",
        "3": "Rent", "4": "Utilities", "5": "Shopping", "6": "Other"
    }

    expenses = {cat: [] for cat in category_map.values()}
    print("\n📥 Start entering your expenses. Type 'q' when you're done.\n")

    while True:
        print("Select an expense category:")
        for key, value in category_map.items():
            print(f"{key} - {value}")
        category_input = input("Enter the category number or 'q' to quit: ").strip().lower()

        if category_input == 'q':
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

        description = input("Add a short description: ") if category == "Other" else None
        timestamp = datetime.now()
        expenses[category].append((amount, description, timestamp))
        print(f"✅ {category} expense of {currency}{amount:.2f} added.\n")

    return expenses


def calculate_total(expenses):
    return sum(amount for items in expenses.values() for amount, _, _ in items)


def show_summary(expenses, currency, income, monthly, weekly, daily):
    total = calculate_total(expenses)
    remaining = income - total

    print("\n🧾 Final Summary")
    print(f"💰 Total Expenses This Session: {currency}{total:.2f}")
    print(f"💰 Remaining Income: {currency}{remaining:.2f}")
    print(f"💰 Monthly Budget: {currency}{monthly:.2f}")
    print(f"💰 Weekly Budget: {currency}{weekly:.2f}")
    print(f"💰 Daily Budget: {currency}{daily:.2f}")

    print("\n🧮 Budget Evaluation:")
    print_budget_eval("Monthly", total, monthly, currency)
    print_budget_eval("Weekly", total, weekly, currency)
    print_budget_eval("Daily", total, daily, currency)

    # Time-based totals from this session
    today = datetime.today().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    today_total = 0
    week_total = 0
    month_total = 0

    for items in expenses.values():
        for amount, _, timestamp in items:
            date = timestamp.date()
            if date == today:
                today_total += amount
            if week_start <= date <= today:
                week_total += amount
            if month_start <= date <= today:
                month_total += amount

    print(f"\n📅 Today's Date: {today}")
    print(f"📅 Week Start Date: {week_start}")
    print(f"📅 Month Start Date: {month_start}")
    print(f"📅 Total Expenses Today: {currency}{today_total:.2f}")
    print(f"📅 Total Expenses This Week: {currency}{week_total:.2f}")
    print(f"📅 Total Expenses This Month: {currency}{month_total:.2f}")


def print_budget_eval(label, total, budget, currency):
    if total > budget:
        print(f"⚠️ {label} budget exceeded by {currency}{total - budget:.2f}")
    else:
        print(f"✅ {label} budget OK (Remaining: {currency}{budget - total:.2f})")


def show_breakdown(expenses, currency):
    print("\n📂 Expenses by Category:")
    for category, items in expenses.items():
        print(f"\n{category}:")
        for amount, desc, _ in items:
            note = f" → {desc}" if desc else ""
            print(f"  - {currency}{amount:.2f}{note}")
        total_cat = sum(amount for amount, _, _ in items)
        print(f"  Total: {currency}{total_cat:.2f}")


def save_to_db(expenses):
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
    for category, entries in expenses.items():
        for amount, desc, timestamp in entries:
            cursor.execute(
                "INSERT INTO expenses (category, amount, description, date) VALUES (?, ?, ?, ?)",
                (category, amount, desc, timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            )
    conn.commit()
    conn.close()


# ------------------------- Main Program -------------------------

def main():
    print("💵 Welcome to the Expense Tracker!")

    currency = get_currency()
    income, monthly_budget = get_income_and_budget(currency)

    default_daily, default_weekly = calculate_budgets(monthly_budget)

    print("\n💡 Smart Budget Suggestions:")
    print(f"  ➤ Suggested weekly budget: {currency}{default_weekly:.2f}")
    print(f"  ➤ Suggested daily budget: {currency}{default_daily:.2f}\n")

    daily_budget, weekly_budget = get_custom_budgets(default_daily, default_weekly)

    expenses = input_expenses(currency)
    print("\n✅ All expenses recorded.")

    show_summary(expenses, currency, income, monthly_budget, weekly_budget, daily_budget)
    show_breakdown(expenses, currency)
    save_to_db(expenses)

    print("\n🎉 Thank you for using the Expense Tracker!")


if __name__ == "__main__":
    main()
