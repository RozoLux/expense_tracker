import psycopg2

dbname = "expense_tracker"
user = "postgres"
password = "8954"
host = "localhost"
port = "5432"

# Establish a connection
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor object to execute SQL queries
cur = conn.cursor()


# Example: Fetch all users
cur.execute("SELECT * FROM Users")
users = cur.fetchall()
print("Users:")
for user in users:
    print(user)

# Insert a new expense    
user_id = 1
amount = 75.00
description = "Dinner"
date = "2023-02-01"
category_id = 3
cur.execute("INSERT INTO Expenses (UserID, Amount, Description, Date, CategoryID) VALUES (%s, %s, %s, %s, %s)",
            (user_id, amount, description, date, category_id))

conn.commit()
print("Expense added successfuly.")

# Example : update an expense
# new_amount = 80.00
# cur.execute("UPDATE Expenses SET Amount = %s WHERE Description = %s", ( new_amount, "Dinner"))
# conn.commit()
# print("Expense updated successfully")
    
# Example : Delete an expense
# cur.execute("DELETE FROM Expenses WHERE Description = %s", ("Dinner",))
# conn.commit()
# print("Expense deleted successfully.")




# Close the cursor and connection
cur.close()
conn.close()