import os
import csv

def saved_goal(amount):
    with open('goal.txt','w') as file:
        file.write(str(amount))

def load_goal():
    if os.path.exists('goal.txt'):
        with open('goal.txt', 'r') as file:
            return float(file.read())
    return 0.0

def custom_value(percent):
    with open('value.txt', 'w') as file:
        file.write(str(percent))

def load_custom_value():
    if os.path.exists('value.txt'):
        with open('value.txt', 'r') as file:
            return float(file.read())
    return 0.0

import datetime
def expense_data():
    price= float(input("Put in the price"))
    expense_category= input("Expense Category")
    date= input("Date")
    if not date:
        date= datetime.date.today().strftime("%d-%m-%Y")
    return price, expense_category, date


def view_data(goal, percent):
    if not os.path.exists('expenses.csv'):
        print("No expenses found yet.")
        return goal, percent
    header = f"{'Date':<12} | {'Category':<15} | {'Amount':<10}"
    print(header)
    print("-" * len(header))
    total = 0
    with open('expenses.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if not row: continue
            date = row[0]
            expense_category = row[1]
            amount = float(row[2])
            print(f"{date:<12} | {expense_category[:15]:<15} | {amount:<10}")
            total += amount
    goal_num = float(goal)
    percent_num = float(percent)
    total_num = float(total)
    warning = (total_num / goal_num) * 100
    remaining_budget = goal_num - total_num
    print(f"Total spent:{round(float(total))}")
    print(f"Remaining budget:{round(float(remaining_budget))}")
    if warning >= 100:
        print("You are over budget")
    elif warning >= percent_num:
        print(f"(reminder) You have spent {warning:.2f}% of your budget")
        print(f"Your current reminder is at{percent_num}%")
    elif warning >= 90:
        print("You've spent over 90% of your budget")
    elif warning >= 75:
        print("You've spent over 75% of your budget")
    else:
        print(f"You've spent {warning:.2f}% of your budget")
    return remaining_budget, warning

def saved_data(date, expense_category, price):
    file_exists = os.path.exists('expenses.csv')
    with open('expenses.csv', 'a') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Category", "Price"])
        writer.writerow([date, expense_category, price])

def clear_data():
    if os.path.exists('expenses.csv'):
        os.remove('expenses.csv')

current_goal= load_goal()
current_percent= load_custom_value()

while True:
    print("1.Add expense 2.Change/set monthly goal 3.View expenses 4.Change custom percentage 5.Clear data 6.Exit")
    choice = input("Select an option (type the number)")
    if choice == '1':
        p, c, d = expense_data()
        saved_data(d, c, p)
        print(current_goal)
    elif choice == '2':
        new_goal=float(input("What is the new goal?"))
        saved_goal(new_goal)
        current_goal= new_goal
        print(current_goal)
    elif choice == '3':

        view_data(current_goal,current_percent)
    elif choice == '4':
        print("***The value you put is percentage spent not percentage left, put in the opposite. For example if you want 20% left to be limit set value at 80%***")
        new_custom_value= float(input("New custom value (must be percentage spent)"))
        custom_value(new_custom_value)
        current_percent= new_custom_value
    elif choice == '5':
        confirmation= input("Are you sure? This can't be undone (Y/N)").lower().strip()
        if confirmation == 'y':
            clear_data()
            print("Data cleared")
        else:
            print("Cancelling")
    else:
        break

