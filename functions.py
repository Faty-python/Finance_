from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import config
import pycountry
import re

def get_database_connection():
    db = sqlite3.connect('user_database.db')
    cursor = db.cursor()
    return db, cursor

def close_database_connection(db):
    if db:
        db.close()

def test_buttons():
    print("Button is working bro!")

def toggle_password(p_block, show_password_var):
    if show_password_var.get():
        p_block.configure(show="")
    else:
        p_block.configure(show="*")
        
def registered_success(email, message):
    smtp_server = config.smtp_server
    smtp_port = config.smtp_port
    smtp_username = config.smtp_username  
    smtp_password = config.smtp_password 
    
    
    sender_email = config.sender_email
    recipient_email = email
    subject = "A New Account Created successfully"
    message = f"The following a new account was created successfully your password is: {message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(sender_email, recipient_email, msg.as_string())

    server.quit()
        
def send_mail_transaction(email, message):
    smtp_server = config.smtp_server
    smtp_port = config.smtp_port
    smtp_username = config.smtp_username  
    smtp_password = config.smtp_password 
    
    
    sender_email = config.sender_email
    recipient_email = email
    subject = "A New Transaction Has been Made"
    message = f"The following Transaction was made: {message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(sender_email, recipient_email, msg.as_string())

    server.quit()

def send_password_reset_email(email, temporary_password):
    smtp_server = config.smtp_server
    smtp_port = config.smtp_port
    smtp_username = config.smtp_username  
    smtp_password = config.smtp_password  

    sender_email = config.sender_email
    recipient_email = email
    subject = "Password Reset"
    message = f"Your temporary password is: {temporary_password}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(sender_email, recipient_email, msg.as_string())

    server.quit()

def generate_temporary_password(length=8):
    characters = string.ascii_letters + string.digits
    temporary_password = ''.join(random.choice(characters) for letters in range(length))
    return temporary_password

def check_pay(credit, amount_pay, debit, name1, purpose, email, balance):
    
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Debit_Account TEXT,
                Credit_Account TEXT,
                Amount TEXT,
                Ben_name TEXT,
                Purpose TEXT,
                Timestamp TIMESTAMP,
                email TEXT
            )
        ''')
        cursor.execute('SELECT * FROM Accounts WHERE Email = ?', (email,))
        existing_account = cursor.fetchone()
        if not existing_account:
            print("Error: Debit account doesn't exist")
            return False
        else:
            cursor.execute('SELECT * FROM Accounts WHERE Account =?', (credit,))
            existing_credit = cursor.fetchone()
            if not existing_credit:
                print("Error: The credit account doesn't exit")
                return False
            else:
                update_query = "UPDATE Accounts SET Balance= ? WHERE Email = ?"
                cursor.execute(update_query, (int(balance) - int(amount_pay), email))
                db.commit()
                update_query = "UPDATE Accounts SET Balance= ? WHERE Account = ?"
                cursor.execute(update_query, (int(balance) + int(amount_pay), credit))
                db.commit()
                cursor.execute('''
                    INSERT INTO Transactions (Debit_Account, Credit_Account, Amount, Ben_name, Purpose, Timestamp, email)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (debit, credit, amount_pay, name1, purpose, datetime.now(), email))

                db.commit()

        return True  

    except sqlite3.IntegrityError:
        return False  

    finally:
        close_database_connection(db)
        
def add_account(email, account, balance, name, phone, acc_type):
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT,
                Account TEXT UNIQUE,
                Balance INTEGER,
                name TEXT,
                Phone TEXT,
                Account_type TEXT
            )
        ''')
        
        cursor.execute('SELECT * FROM Accounts WHERE Email = ?', (email,))
        existing_account = cursor.fetchone()
        if existing_account:
            print("Error: Email address already exists.")
            return False
        else:
            cursor.execute('''
            INSERT INTO Accounts (Email, Account, Balance, Name, Phone, Account_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, account, balance, name, phone, acc_type))

        db.commit()

        return True  

    except sqlite3.IntegrityError:
        return False  

    finally:
        close_database_connection(db)
        
        
def deposit_transaction(email, account, balance, deposit, name):
    db, cursor = get_database_connection()
    purpose = 'Deposit'
    try:
        update_query = "UPDATE Accounts SET Balance= ? WHERE Email = ?"
        cursor.execute(update_query, (int(balance) + int(deposit), email))
        cursor.execute('''
            INSERT INTO Transactions (Debit_Account, Credit_Account, Amount, Ben_name, Purpose, Timestamp, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (account, account, deposit, name, purpose, datetime.now(), email))
        db.commit()
        return True
    
    except sqlite3.IntegrityError:
        return False  

    finally:
        close_database_connection(db)
        
        
def withdrawal_transaction(email, account, balance, deposit, name):
    db, cursor = get_database_connection()
    purpose = 'Withdrawal'
    try:
        update_query = "UPDATE Accounts SET Balance= ? WHERE Email = ?"
        cursor.execute(update_query, (int(balance) - int(deposit), email))
        cursor.execute('''
            INSERT INTO Transactions (Debit_Account, Credit_Account, Amount, Ben_name, Purpose, Timestamp, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (account, account, deposit, name, purpose, datetime.now(), email))
        db.commit()
        return True
    
    except sqlite3.IntegrityError as e:
        print(e)
        return False  

    finally:
        close_database_connection(db)

def check_login(username, password):
    db, cursor = get_database_connection()
    try:

        cursor.execute("SELECT email, password FROM Users WHERE email = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            
            return True

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        close_database_connection(db)

    return False


def save_budget(email1, number1, balance, amount, purpose):
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            INSERT INTO Budget (Email, Account, Balance, Amount, Purpose, Timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email1, number1, balance, amount, purpose, datetime.now()))

        db.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        
        
def save_invest(email1, number1, balance, amount, purpose, years):
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            INSERT INTO Investment (Email, Account, Balance, Amount, Purpose, Years_Invested, TIMESTAMP)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email1, number1, balance, amount, purpose, years, datetime.now()))

        db.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        
        
def save_asset(email1, number1, balance, atype, aname, amount):
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            INSERT INTO Assets (Email, Account, Balance, Asset_Type, Asset_name, Asset_Amount, TIMESTAMP)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (email1, number1, balance, amount, atype, aname, datetime.now()))

        db.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)
        
def count_emails_in_string(input_string):
    emails = [email for email in input_string.split(";") if email.strip()]
    return len(emails)
        
def group_save(email1, atype, purpose, aname):
    db, cursor = get_database_connection()
    if aname != "" and aname != "Select Emails":
        try:
            cursor.execute('''
            INSERT INTO BGroup (Email, Group_Name, Group_Purpose, Group_members, Total_members, TIMESTAMP)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email1, atype, purpose, aname, count_emails_in_string(aname), datetime.now()))
            
            email_list = [email.strip() for email in aname.split(';') if email.strip()]
            for email in email_list:
                cursor.execute(
                    "SELECT Group_IN FROM budget WHERE Email = ?", 
                    (email,)
                )
                current_value = cursor.fetchone()

                if current_value and current_value[0]:  
                    updated_value = f"{current_value[0]};{atype}"
                else:  
                    updated_value = atype
                cursor.execute(
                    "UPDATE budget SET Group_IN = ? WHERE Email = ?", 
                    (updated_value, email)
                )
            db.commit()
            return True
        except sqlite3.Error as e:
            print("SQLite error:", e)
    else:
        return False
        


def register_user(first_name, last_name, country, username, email, password, security_question, security_answer):
    db, cursor = get_database_connection()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                first_name TEXT,
                last_name TEXT,
                country TEXT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                security_question TEXT,
                security_answer TEXT
            )
        ''')

        cursor.execute('''
            INSERT INTO Users (first_name, last_name, country, username, email, password, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, country, username, email, password, security_question, security_answer.lower()))

        db.commit()

        return True  

    except sqlite3.IntegrityError:
        return False  

    finally:
        close_database_connection(db)
        


def email_exists(email):
    db, cursor = get_database_connection()
    try:
        cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
        user = cursor.fetchone()

        return user

    finally:
        close_database_connection(db)


def get_countries():
    country_names_unsorted = [country.name for country in pycountry.countries]
    country_names = sorted(country_names_unsorted)
    return country_names


def validate_country(country_name):
    available_countries = get_countries()
    return country_name in available_countries

def update_password(email, temporary_password):
    db, cursor = get_database_connection()
    try:
        update_query = "UPDATE Users SET password = ? WHERE email = ?"
        cursor.execute(update_query, (temporary_password, email))
        db.commit()

        return True 

    except Exception as e:
        print("Error updating password:", str(e))
        return False  

    finally:
        close_database_connection(db)
        
        
def password_save(email, atype):
    db, cursor = get_database_connection()
    try:
        update_query = "UPDATE Users SET password = ? WHERE email = ?"
        cursor.execute(update_query, (atype, email))
        db.commit()

        return True 

    except Exception as e:
        print("Error updating password:", str(e))
        return False  

    finally:
        close_database_connection(db)


def get_security_question(email):
    db, cursor = get_database_connection()
    try:
        cursor.execute("SELECT security_question FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None  

    except sqlite3.Error as e:
        print("Database error:", str(e))
        return None
    finally:
        close_database_connection(db)

def check_security_answer(email, provided_answer):
    db, cursor = get_database_connection()
    try:
        cursor.execute("SELECT security_answer FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()

        if result:
            stored_answer = result[0]
            if provided_answer.lower() == stored_answer.lower():
                return True 
            else:
                return False  
        else:
            return False  

    except sqlite3.Error as e:
        print("Database error:", str(e))
        return False
    finally:
        close_database_connection(db)

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def is_valid_chars(input_string):
    pattern = re.compile(r'^[a-zA-Z0-9_\-]+$')
    return pattern.match(input_string) is not None

def is_valid_chars_space(input_string):
    pattern = re.compile(r'^[a-zA-Z0-9_\- ]+$')
    return pattern.match(input_string) is not None
