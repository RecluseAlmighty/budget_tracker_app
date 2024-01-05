import sqlite3

db = sqlite3.connect('budget_tracker') # Connecting to the database 'budget_tracker'

cursor = db.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS finances (
    id INTEGER PRIMARY KEY, 
    income_category TEXT, 
    expense_category TEXT, 
    income INTEGER, 
    expense INTEGER, 
    expense_name TEXT, 
    budget INTEGER, 
    finance_goal TEXT,
    goal_amount INTEGER, 
    goal_fund INTEGER, 
    UNIQUE(id, income_category, expense_category, income, expense, expense_name, budget, finance_goal, goal_amount, goal_fund))
''') # Creating the table for the finances..
db.commit()

def add_expense(): # Add expense function..
    
    try:

        db = sqlite3.connect('budget_tracker')
    
        cursor = db.cursor()

        expense = input("\nPlease enter the amount of the expense you would like to add to the database: ")

        expense_name = input("\nPlease enter a name for the expense: ").lower()

        expense_cat = input("\nPlease enter the category of the expense: ").lower()
        
        cursor.execute('''INSERT OR REPLACE INTO finances (expense, expense_name,  expense_category)
                VALUES (?, ?, ?)''', (expense, expense_name, expense_cat,))
        
        db.commit()
        
        print(f"\nThe {expense_cat} expense {expense_name} of £{expense} has now been added to the database!")
    
    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like something has gone wrong.")
        raise DatabaseError
    finally:
        db.close()

def view_expenses(): # View expenses function..
    
    db = sqlite3.connect('budget_tracker')
        
    cursor = db.cursor()
        
    cursor.execute('''SELECT expenses, expense_name, expenses_category FROM finances''')
    all_expenses = cursor.fetchall()
    print(f"\n{all_expenses}")
    db.close()

def update_expenses():

    try:

        chosen_expense = input("What is the name of the expense you would like to update: ").lower()

        db = sqlite3.connect('budget_tracker')

        cursor = db.cursor()

        cursor.execute('''SELECT expense_name, expense FROM finances WHERE expense_name = ? ''', (chosen_expense,))
        current_expense_amt = cursor.fetchall()
        print(f"The current amount of this expense: {current_expense_amt}")

        fund_update = input(f"\nEnter the amount you want to update thos expense to: ")

        cursor.execute('''UPDATE finances SET expense = ? WHERE expense_name = ? ''', (fund_update, chosen_expense,))
        
        db.commit()

        print(f"Your {chosen_expense} expense was updated to £{fund_update}!")

    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like this expense does not exist yet..")
        raise DatabaseError
    finally:
        db.close()


def view_expense_by_cat():

    db = sqlite3.connect('budget_tracker')

    cursor = db.cursor()

    cursor.execute('''SELECT expense_category, SUM(expense) FROM finances GROUP BY expense_category''')

    results = cursor.fetchall()

    for row in results:
        print(f"{row[0]}: £{row[1]}")
        #print(f"{row[0]}: £{str(row[1])}")

    db.close()


def add_income(): # Add income function..
    
    try:

        
        db = sqlite3.connect('budget_tracker')
    
        cursor = db.cursor()

        income = input("\nPlease enter the income you would like to add to the database: ")

        income_cat = input("\nPlease enter the category of the income: ").lower()
        
        cursor.execute('''INSERT OR REPLACE INTO finances (income, income_category)
                VALUES (?, ?)''', (income, income_cat,))
        
        db.commit()
        
        print(f"\nThe {income_cat} income of £{income} has now been added to the database!")
    
    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like something has gone wrong.")
        raise DatabaseError
    finally:
        db.close()

def view_income(): # View income function..
    
    db = sqlite3.connect('budget_tracker')
        
    cursor = db.cursor()
        
    cursor.execute('''SELECT income, income_category FROM finances''')
    all_income = cursor.fetchall()
    print(f"\n{all_income}")
    db.close()

def view_income_by_cat():

    db = sqlite3.connect('budget_tracker')

    cursor = db.cursor()

    cursor.execute('''SELECT income_category, SUM(income) FROM finances GROUP BY income_category''')

    results = cursor.fetchall()

    for row in results:
        print(f"{row[0]}: £{row[1]}")
        #print(f"{row[0]}: £{str(row[1])}")

    db.close()

def set_budget_for_cat():

    try:

        db = sqlite3.connect('budget_tracker')
    
        cursor = db.cursor()

        expense_cat = input("\nWhich category would you like to make a budget for: ").lower()

        set_budget = input(f"\nPlease enter your budget for the {expense_cat} budget: ")

        cursor.execute('''UPDATE finances SET budget = ? WHERE expense_category = ? ''', (set_budget, expense_cat))
        
        db.commit()
        
        print(f"\nThe £{set_budget} budget for {expense_cat} has now been added to the database!")
    
    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like you have already set this budget previously or the category does not exist.")
        raise DatabaseError
    finally:
        db.close()

def view_budget_for_cat():

    db = sqlite3.connect('budget_tracker')

    cursor = db.cursor()

    user_cat_search = input("Which category of expense budget would you like to view: ").lower()

    cursor.execute('''SELECT budget FROM finances WHERE expense_category = ?''', (user_cat_search, ))

    results = cursor.fetchone()

    for row in results:
        print(f"{row[1]}: £{row[0]}")
        #print(f"{row[0]}: £{str(row[1])}")

    db.close()

def set_finance_goal():

    db = sqlite3.connect('budget_tracker')

    cursor = db.cursor()

    goal_name = input("What is the name of your financial goal (eg. house down payment, paying off debt or for retirement): ").lower()

    goal_amount = input(f"Enter your {goal_name} goal amount: ")

    cursor.execute('''INSERT OR REPLACE INTO finances (finance_goal, goal_amount)
                VALUES (?, ?)''', (goal_name, goal_amount,))
    
    db.commit()
    
    db.close()

def add_goal_funds():

    try:

        chosen_finance_goal = input("What is the name of the financial goal you would like to add funds to: ").lower()

        db = sqlite3.connect('budget_tracker')

        cursor = db.cursor()

        incoming_funds = input(f"Enter the amount of funds to add to your goal: ")

        cursor.execute('''UPDATE finances SET goal_fund = ? WHERE finance_goal = ? ''', (incoming_funds, chosen_finance_goal,))
        
        db.commit()

        print(f"£{incoming_funds} was added to your {chosen_finance_goal} finance goal. Well done!! ")

    except Exception as DatabaseError:
        db.rollback()
        print("\nOops. Looks like you dont have that goal set up yet..")
        raise DatabaseError
    finally:
        db.close()


def view_goal_progress():

    try:

        chosen_goal = input("Which financial goal would you like to view the progress of: ").lower()

        db = sqlite3.connect('budget_tracker')

        cursor = db.cursor()

        cursor.execute('''SELECT finance_goal, goal_amount, goal_fund, (goal_amount - goal_fund) AS difference FROM finances WHERE finance_goal = ? ''', (chosen_goal,))
        goal_progress = cursor.fetchone()

        for row in goal_progress:
            print(f"{row[0]}: £{row[2]}\t Goal:£{row[1]}\t You have £{row[3]} left till you reach your goal! ")

    except Exception as DatabaseError:
        db.rollback()
        print("Oops. Looks like you dont have that goal set up yet.")
        raise DatabaseError
    finally:
        db.close()

while True:
    # Present the menu to the user
    menu = input('''\nSelect one of the following options:
    1. Add expense
    2. View expenses
    3. Update expenses
    4. View expenses by category
    5. Add income
    6. View income
    7. View income by category
    8. Set budget for a category
    9. View budget for a category
    10. Set financial goals
    11. Add funds to a financial goal
    12. View progress towards financial goals
    13. Quit
    : ''')

    if menu == '1':
        add_expense()

    elif menu == '2':
        view_expenses()

    elif menu == '3':
        update_expenses()

    elif menu == '4':
        view_expense_by_cat()

    elif menu == '5':
        add_income()

    elif menu == '6':
        view_income()

    elif menu == '7':
        view_income_by_cat()

    elif menu == '8':
        set_budget_for_cat()

    elif menu == '9':
        view_budget_for_cat()

    elif menu == '10':
        set_finance_goal()

    elif menu == '11':
        add_goal_funds()

    elif menu == '12':
        view_goal_progress()

    elif menu == '13':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made entered an invalid input. Please try again")