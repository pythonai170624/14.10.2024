# pip install psycopg2
# pip install cryptography
# pip install bcrypt psycopg2-binary
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="hw_26_09_24",
    user="admin",
    password="admin",
    port=5556
)

import psycopg2
from psycopg2 import sql

# Connect to PostgreSQL
try:
    conn.autocommit = False  # Ensure autocommit is disabled for transactions
    cursor = conn.cursor()

    # Step 1: Drop the accounts table if it already exists
    cursor.execute("DROP TABLE IF EXISTS accounts")

    # Step 2: Create the accounts table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id SERIAL PRIMARY KEY,
        account_name VARCHAR(100),
        balance DECIMAL(10, 2)
    );
    """
    cursor.execute(create_table_query)

    # Step 3: Insert initial data into the accounts table
    insert_data_query = """
    INSERT INTO accounts (account_name, balance) VALUES
    ('Alice', 1000.00),
    ('Bob', 500.00),
    ('Charlie', 2000.00);
    """
    cursor.execute(insert_data_query)
    conn.commit()  # Commit the creation and data insertion

    print("Table 'accounts' created and data inserted successfully.")

    # Step 4: Define the function to perform a money transfer between accounts
    def transfer_money(account_from, account_to, amount):
        try:
            print("Transaction started")

            # Withdraw from account_from
            cursor.execute(
                sql.SQL("UPDATE accounts SET balance = balance - %s WHERE account_id = %s"),
                (amount, account_from)
            )

            # Check if the withdrawal succeeded (balance should not be negative)
            cursor.execute(
                sql.SQL("SELECT balance FROM accounts WHERE account_id = %s"),
                (account_from,)
            )
            balance = cursor.fetchone()[0]
            if balance < 0:
                raise Exception(f"Insufficient funds in account {account_from}")

            # Deposit to account_to
            cursor.execute(
                sql.SQL("UPDATE accounts SET balance = balance + %s WHERE account_id = %s"),
                (amount, account_to)
            )

            # Commit the transaction
            conn.commit()
            print(f"Transaction committed: Transferred {amount} from account {account_from} to account {account_to}")

        except Exception as e:
            # If an error occurs, rollback the transaction
            conn.rollback()
            print(f"Transaction failed: {e}")

    # Step 5: Perform a money transfer from Alice (account 1) to Bob (account 2)
    transfer_money(1, 2, 200)

    # Step 6: Verify the balances after the transaction
    cursor.execute("SELECT account_id, account_name, balance FROM accounts")
    accounts = cursor.fetchall()
    print("\nAccount balances after the transaction:")
    for account in accounts:
        print(f"Account {account[1]} (ID: {account[0]}), Balance: {account[2]:.2f}")

except Exception as error:
    print(f"Error: {error}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()


'''
-- First, let's create a procedure for transferring money between accounts
CREATE OR REPLACE PROCEDURE transfer_funds(
    account_from INT,
    account_to INT,
    amount DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Start transaction (Note: not explicitly required inside procedures)
    BEGIN
        -- Withdraw from account_from
        UPDATE accounts
        SET balance = balance - amount
        WHERE account_id = account_from;

        -- Check if the withdrawal succeeded (balance should not be negative)
        IF (SELECT balance FROM accounts WHERE account_id = account_from) < 0 THEN
            RAISE EXCEPTION 'Insufficient funds in account %', account_from;
        END IF;

        -- Deposit to account_to
        UPDATE accounts
        SET balance = balance + amount
        WHERE account_id = account_to;

        -- Commit the transaction
        COMMIT;
    EXCEPTION
        -- If there's any error, rollback the transaction
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END;
END;
$$;

'''