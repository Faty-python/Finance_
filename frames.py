from datetime import datetime
import sqlite3
import tkinter
import customtkinter
from functions import add_account, check_pay, close_database_connection, deposit_transaction, get_database_connection, group_save, is_valid_chars_space, is_valid_chars, check_security_answer, get_security_question, is_valid_email, get_countries, password_save, registered_success, save_asset, save_budget, save_invest, send_mail_transaction, toggle_password, register_user, test_buttons, check_login, generate_temporary_password, send_password_reset_email, email_exists, update_password, withdrawal_transaction
from PIL import ImageTk, Image
from tkinter import E, END, Toplevel, messagebox, ttk
from CTkMenuBar import *
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.cm import get_cmap

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_login_frame()
        

    def setup_login_frame(self):

        self.login_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        
        self.text = customtkinter.CTkLabel(master=self.login_frame, text="Log Into Account", font=('Century Gothic', 25))
        self.text.place(x=50, y=45)

        self.error_label = customtkinter.CTkLabel(master=self.login_frame, text="", font=('Century Gothic', 12), text_color="red")
        self.error_label.place(x=25, y=80)

     
        self.u_block = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text="Email address")
        self.u_block.place(x=50, y=110)

       
        self.show_password_var = customtkinter.BooleanVar()
        self.p_block = customtkinter.CTkEntry(master=self.login_frame, width=220, placeholder_text="Password", show="*")
        self.p_block.place(x=50, y=150)

        self.show_password = customtkinter.CTkCheckBox(master=self.login_frame, text="Show Password", font=('Century Gothic', 12), command=lambda: toggle_password(self.p_block, self.show_password_var), variable=self.show_password_var)
        self.show_password.place(x=50, y=190)
        self.label3 = customtkinter.CTkLabel(master=self.login_frame, text="Forgot password?", font=('Century Gothic', 10))
        self.label3.place(x=180, y=180)
        self.label3.bind("<Enter>", lambda event: self.label3.configure(cursor="hand2"))
        self.label3.bind("<Leave>", lambda event: self.label3.configure(cursor="arrow"))
        self.label3.bind("<Button-1>", lambda event: self.master.open_forgot_password_frame())


        self.login_button = customtkinter.CTkButton(master=self.login_frame, width=100, text="Login", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.check_login_credentials)
        self.login_button.place(x=110, y=230)
        
        self.register_button = customtkinter.CTkButton(master=self.login_frame, width=100, text="Register", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.master.open_register_frame)
        self.register_button.place(x=110, y=270)
        
        self.g_logo = customtkinter.CTkImage(Image.open("images/g.png").resize((20, 20), Image.LANCZOS))
        self.fb_logo = customtkinter.CTkImage(Image.open("images/fb.png").resize((20, 20), Image.LANCZOS))

        self.g_button = customtkinter.CTkButton(master=self.login_frame, width=100, image=self.g_logo, text="Google", corner_radius=6, fg_color="white", text_color="black", compound="left", hover_color="#f0f0f0", anchor="w", command=test_buttons)
        self.g_button.place(x=10, y=340)

        self.fb_button = customtkinter.CTkButton(master=self.login_frame, width=100, image=self.fb_logo, text="Facebook", corner_radius=6, fg_color="white", text_color="black", compound="left", hover_color="#f0f0f0", anchor="w", command=test_buttons)
        self.fb_button.place(x=210, y=340)

    def check_login_credentials(self):
        email = self.u_block.get()
        password = self.p_block.get()
        if check_login(email, password):
            self.master.open_loggedin_frame(email)
        else:
            self.error_label.configure(text="Invalid username or password. Please try again.")

class RegisterFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.setup_register_frame()

    def setup_register_frame(self):
        self.master.change_title("Registration")
        self.registration_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.registration_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.back_button = customtkinter.CTkButton(
            master=self,
            width=30,
            height=30,
            text="◀️",  
            corner_radius=6,
            fg_color="#3498db",
            text_color="#ffffff",
            hover_color="#2980b9",
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)
        self.name_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="First Name")
        self.name_entry.place(x=50, y=50)

        self.surname_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Last Name")
        self.surname_entry.place(x=50, y=80)
        self.country_var = customtkinter.StringVar(value="Select Country")
        self.country_box = customtkinter.CTkComboBox(master=self.registration_frame, variable=self.country_var, values=get_countries(),
                                                          width=220, state="readonly")
        self.country_box.place(x=50, y=110)

        self.username_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Username")
        self.username_entry.place(x=50, y=140)

        self.email_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Enter your email")
        self.email_entry.place(x=50, y=170)

        self.p_block = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Choose a password", show="*")
        self.p_block.place(x=50, y=200)

        self.security_question_label = customtkinter.CTkLabel(master=self.registration_frame, text="Security Question", font=('Century Gothic', 10))
        self.security_question_label.place(x=50, y=230)

        self.security_questions = ["What is your mother's maiden name?", "What is your favorite pet's name?", "Where were you born?", "What is your favorite movie?", "What is your favorite book?"]
        self.security_question_var = customtkinter.StringVar(value="Select Security Question")
        self.security_question_dropdown = customtkinter.CTkComboBox(master=self.registration_frame, variable=self.security_question_var, values=self.security_questions, width=220, state="readonly")
        self.security_question_dropdown.place(x=50, y=260)
        self.security_answer_entry = customtkinter.CTkEntry(master=self.registration_frame, width=220, placeholder_text="Security Answer")
        self.security_answer_entry.place(x=50, y=290)
        self.register_button = customtkinter.CTkButton(master=self.registration_frame, width=100, text="Register",
                                                  corner_radius=6,
                                                  fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9",
                                                  command=self.new_user_data)
        self.register_button.place(x=110, y=340)

    def new_user_data(self):
        first_name = self.name_entry.get()
        last_name = self.surname_entry.get()
        country = self.country_box.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.p_block.get()
        security_question = self.security_question_var.get()  
        security_answer = self.security_answer_entry.get()

        if not first_name or not last_name or not username or not password:
            print("Please fill in all required fields.")
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        if not is_valid_chars_space(first_name) or not is_valid_chars_space(last_name):
            print("Name and Surname must contain only English letters.")
            messagebox.showerror("Error", "Use Only English letters.")
            return
        if not is_valid_chars(username) or not is_valid_chars(password):
            print("Fields must contain only English letters and standard characters.")
            messagebox.showerror("Error", "Use Only English letters and standard characters without spaces.")
            return
        if country == "Select Country":
            print("No country Selected")
            messagebox.showerror("Error", "Please select a country.")
            return
        if security_question == "Select Security Question":
            print("Invalid Security Question")
            messagebox.showerror("Error", "Invalid Security Question.")
            return
        if not is_valid_email(email):
            print("Invalid email address")
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if register_user(first_name, last_name, country, username, email, password, security_question, security_answer):
            print("Registration successful!")
            message = password
            registered_success(email, message)
            messagebox.showinfo("Success", "Registration was successful!")
            self.registration_frame.place_forget()
            self.master.open_main_frame()
            return
        else:
            print("Username or email is already in use.")
            messagebox.showerror("Error", "The username or e-mail already exists.")
            return


class ForgotPasswordFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.setup_forgot_password_frame() 

    def setup_forgot_password_frame(self): 
        self.master.change_title("Forgot Password")
        self.forgot_password_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.forgot_password_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.back_button = customtkinter.CTkButton(
            master=self,
            width=30,
            height=30,
            text="◀️",  
            corner_radius=6,
            fg_color="#72bcd4",
            text_color="#1e5364",
            hover_color="#e8f4f8",
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        self.text = customtkinter.CTkLabel(master=self.forgot_password_frame, text="Enter Your E-Mail", font=('Century Gothic', 25))
        self.text.place(x=50, y=45)
        self.email_block = customtkinter.CTkEntry(master=self.forgot_password_frame, width=220, placeholder_text="Email")
        self.email_block.place(x=50, y=110)
        self.submit_button = customtkinter.CTkButton(master=self.forgot_password_frame, width=100, text="Submit", corner_radius=6, fg_color="#72bcd4", text_color="#1e5364", hover_color="#e8f4f8", command=self.handle_reset_password)
        self.submit_button.place(x=110, y=230)

    def handle_reset_password(self):
        user_email = self.email_block.get()
        check_exists = email_exists(user_email)
        security_question = get_security_question(user_email)
        if not is_valid_email(user_email):
            print("Invalid email address")
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if check_exists:
            self.master.destroy_all_frames()
            self.master.open_forgot_password_frame2(user_email)
        else:
            messagebox.showerror("Error", "E-Mail doesn't exists!")
            return

class ForgotPasswordFrame2(customtkinter.CTkFrame):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.master = master
        self.user_email = user_email
        self.setup_forgot_password_frame2()

    def setup_forgot_password_frame2(self):
        self.master.change_title("Forgot Password - Step 2")
        self.forgot_password2_frame = customtkinter.CTkFrame(master=self, width=320, height=380)
        self.forgot_password2_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.back_button = customtkinter.CTkButton(
            master=self,
            width=30,
            height=30,
            text="◀️", 
            corner_radius=6,
            fg_color="#72bcd4",
            text_color="#1e5364",
            hover_color="#e8f4f8",
            command=self.master.open_main_frame
        )
        self.back_button.place(x=10, y=10)

        self.text = customtkinter.CTkLabel(master=self.forgot_password2_frame, text="Step 2", font=('Century Gothic', 25))
        self.text.place(x=50, y=45)

        security_question = get_security_question(self.user_email)  
        self.security_question_label = customtkinter.CTkLabel(master=self.forgot_password2_frame, text=security_question, font=('Century Gothic', 14))
        self.security_question_label.place(x=50, y=110)

        self.security_answer_block = customtkinter.CTkEntry(master=self.forgot_password2_frame, width=220, placeholder_text="Security Answer")
        self.security_answer_block.place(x=50, y=160)
        
        self.submit_button2 = customtkinter.CTkButton(master=self.forgot_password2_frame, width=100, text="Reset Password", corner_radius=6, fg_color="#72bcd4", text_color="#1e5364", hover_color="#e8f4f8", command=self.handle_reset_password)
        self.submit_button2.place(x=110, y=230)

    def handle_reset_password(self):
        user_answer = self.security_answer_block.get()

        if check_security_answer(self.user_email, user_answer):  
            temporary_password = generate_temporary_password()
            update_password(self.user_email, temporary_password) 
            send_password_reset_email(self.user_email, temporary_password) 
            messagebox.showinfo("Password Reset", "An email with instructions has been sent to your email address.")
            self.master.destroy_all_frames()
            self.master.open_main_frame()
        else:
            messagebox.showerror("Error", "Security answer does not match.")

class LoggedInFrame(customtkinter.CTkFrame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.user_email = email
        self.setup_loggedin_frame()

    def setup_loggedin_frame(self):
        self.master.change_geometry("1280x720")
        self.master.change_title("Main Page")
        self.setup_loggedin_frame = customtkinter.CTkFrame(master=self, width=1200, height=600, corner_radius=24, bg_color="transparent")
        self.setup_loggedin_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.menubar = CTkMenuBar(master=self)
        # self.menubar.add_cascade('File') 
        # self.menubar.add_cascade('New File') 
        # self.menubar.add_cascade('Open...') 
        # self.menubar.add_cascade('Save')
        self.menubar.add_cascade('Exit', command = self.master.destroy)
        msg = "Welcome to Financial Mgt System: " + self.user_email
        self.text = customtkinter.CTkLabel(master=self.setup_loggedin_frame, text=msg, font=('Times Romans', 25))
        self.text.place(x=20, y=20, anchor="w")
        db, cursor = get_database_connection()
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
        
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Budget (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Email TEXT,
                    Account TEXT,
                    Balance INTEGER,
                    Purpose TEXT,
                    Amount TEXT,
                    Current_Expenses TEXT,
                    Group_IN TEXT NULLABLE,
                    TIMESTAMP TIMESTAMP
                )
            ''')
        
        query = '''
            SELECT Account, Balance
            FROM Accounts
            WHERE Email = ?
        '''
        
        
        query1 = '''
            SELECT SUM(AMOUNT), SUM(CURRENT_EXPENSES)
            FROM Budget
            WHERE Email = ?
        '''
        cursor.execute(query, (self.user_email,))
        
        data = cursor.fetchall()
        
        if data:
            print(data) 
        else:
            self.master.add_account_details(self.user_email)
        customtkinter.CTkLabel(master=self.setup_loggedin_frame, text="Current Balance: ", text_color='green', font=('Arial', 15, 'bold'), padx=20).place(x=20, y=60, anchor="w")
        self.curr_balance_text = customtkinter.CTkEntry(master=self.setup_loggedin_frame, text_color='red')
        for row in data:
            balance = row[1]
        if data:
            if int(balance) < 500:
                messagebox.showwarning("Warning", "Your account balnace is getting lower than 500 please deposit")
            self.curr_balance_text.insert(END, '$' + format(int(balance), '.2f'))
        else:
            self.curr_balance_text.insert(END, '$' + format(0.0, '.2f'))
        self.curr_balance_text.configure(state="disabled")
        self.curr_balance_text.place(x=200, y=50)
        
        for row in data:
            account = row[0]
        if data:
            self.account = account
        headers = ["DEBIT_ACC", "CREDIT_ACC", "Amount", "Purpose", "Time"]
        
        
        query = '''
            SELECT Debit_Account, Credit_Account, Amount, Purpose, Timestamp
            FROM Transactions
            WHERE email = ? or Credit_Account=?
        '''
        if data:
            cursor.execute(query, (self.user_email, self.account, ))
            data = cursor.fetchall()
        
        start_x = 100
        start_y = 100
        cell_width = 150
        cell_height = 30

        for col, header in enumerate(headers):
            x = start_x + col * cell_width
            label = customtkinter.CTkLabel(
                master=self.setup_loggedin_frame,
                text=header,
                font=("Arial", 12, "bold"),
                width=cell_width
            )
            label.place(x=x, y=start_y)
        if data:
            for row_idx, row_data in enumerate(data, start=1):
                for col_idx, cell_data in enumerate(row_data):
                    x = start_x + col_idx * cell_width
                    y = start_y + row_idx * cell_height
                    entry = customtkinter.CTkEntry(
                        master=self.setup_loggedin_frame,
                        justify="center",
                        width=cell_width - 10
                    )
                    entry.insert(0, str(cell_data))  
                    entry.place(x=x, y=y)
        
        else:
            customtkinter.CTkLabel(master=self.setup_loggedin_frame, text="No transactions found for the given account. ", text_color='red', font=('Arial', 15, 'bold'), padx=20).place(x=50, y=150, anchor="w")
                
        
                
        
        self.action_part = customtkinter.CTkFrame(master=self.setup_loggedin_frame, width=300, height=500, corner_radius=24, bg_color="green")
        self.action_part.place(relx = 1, x =-20, y = 60, anchor='ne')  
        customtkinter.CTkLabel(master=self.action_part, text="CHOOSE AN ACTION: ", text_color='red', font=('Arial', 15, 'bold'), padx=20).place(relx = 1, x =-20, y = 60, anchor='e')
        self.new_txn_button = customtkinter.CTkButton(master=self.action_part, 
                                                      hover_color='pink', text="New Transaction", width=240, command=self.add_new_txn)
        self.new_txn_button.place(x =20, y = 100)

        self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
                                                        hover_color='blue', text="Visualize Data", width=240, command=self.visualize)
        self.visualize_button.place(x =20, y = 150)        
        
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='red', text="Deposit", width=240, command=self.deposit)
        self.view_button.place(x =20, y = 200)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='red', text="WithDraw", width=240,
                                                   command=self.withdraw)
        self.view_button.place(x =20, y = 250)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='green', text="Profile", width=240, command=self.set_profile)
        self.view_button.place(x =20, y = 300)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='green', text="Finance Plan", width=240, command=self.set_budget)
        self.view_button.place(x =20, y = 350)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='green', text="Update Password", width=240, command=self.set_password)
        self.view_button.place(x =20, y = 400)
        cursor.execute(query1, (self.user_email,))
        data1 = cursor.fetchall()
        if data:
            for row in data1:
                try:
                    if row[0] is not None and row[1] is not None:
                        if float(row[0]) < float(row[1]):
                            messagebox.showwarning("Warning", "You have spent more than your Budget")
                    else:
                        messagebox.showerror("Error", "Please add your budget")
                except ValueError:
                    messagebox.showerror("Error", "Plan your budget")
                
        else:
            messagebox.showerror("Error", "Please add your budget")
        db.close()
        pass
        
    def add_new_txn(self):
        self.master.new_transaction(self.user_email)
        
    def set_profile(self):
        self.master.add_account_details(self.user_email)
        
    def set_password(self):
        self.master.add_password_details(self.user_email)
        
    def deposit(self):
        self.master.add_new_deposit(self.user_email)
        
    def withdraw(self):
        self.master.add_new_withdrawal(self.user_email)
        
    def visualize(self):
        self.destroy()
        self.master.add_visualization(self.user_email)
        
    def set_budget(self):
        self.destroy()
        self.master.add_budget(self.user_email)
        
class NewTransactionFrame(customtkinter.CTkFrame):
    def __init__(self, master, email):
        super().__init__(master)
        self.master = master
        self.email= email
        self.setup_transaction_frame()
        
    def setup_transaction_frame(self):
        self.setup_transaction_frame = customtkinter.CTkFrame(master=self, width=450, height=450, corner_radius=24, bg_color="cyan")
        self.setup_transaction_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.text = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="New Transaction",
                                           text_color='red', font=('Times Romans', 14))
        self.text.place(x=20, y=20, anchor="w")
        
        self.error_label = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="", font=('Century Gothic', 12), text_color="red")
        self.error_label.place(x=20, y=25)
        
        self.debit = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="Debit Account: ",
                                           text_color='green', font=('Times Romans', 14))
        self.debit.place(x=20, y=60, anchor="w")
        
        self.amount_pay = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="Amount: ",
                                           text_color='green', font=('Times Romans', 14))
        self.amount_pay.place(x=20, y=100, anchor="w")
        
        self.credit = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="Credit Account: ",
                                           text_color='green', font=('Times Romans', 14))
        self.credit.place(x=20, y=140, anchor="w")
        self.text = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="Ben Name: ",
                                           text_color='green', font=('Times Romans', 14))
        self.text.place(x=20, y=180, anchor="w")
        self.ben_name = customtkinter.CTkLabel(master=self.setup_transaction_frame, text="Purpose: ",
                                           text_color='green', font=('Times Romans', 14))
        self.ben_name.place(x=20, y=220, anchor="w")
        self.view_button = customtkinter.CTkButton(master=self.setup_transaction_frame, 
                                                   hover_color='green', text="Transact", width=150
                                                   , command=self.check_amount_inputs)
        self.view_button.place(x =20, y = 265)
        self.view_button2 = customtkinter.CTkButton(master=self.setup_transaction_frame, 
                                                   hover_color='red', text="Cancel", width=150, command=self.close)
        self.view_button2.place(relx = 1, x =-2, y = 260, anchor ='ne')
        db, cursor = get_database_connection()
        
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.email,))
        data = cursor.fetchall()
        if data:
            cursor.execute(query, (self.email,))
            data = cursor.fetchall()
            
            self.debit = customtkinter.CTkEntry(master=self.setup_transaction_frame, placeholder_text='Debit Account', width=180)
            for row in data:
                account_id = row[0]
            self.debit.insert(0, account_id)
            self.debit.configure(state="disabled")
            self.debit.place(relx = 1, x =-20, y = 45, anchor ='ne')
            
            for row in data:
                balance = row[1]
            self.balance = balance
            
            self.amount1 = customtkinter.CTkEntry(master=self.setup_transaction_frame, placeholder_text='0.0', width=180)
            self.amount1.place(relx = 1, x =-20, y = 85, anchor ='ne')
            
            self.credit = customtkinter.CTkEntry(master=self.setup_transaction_frame, placeholder_text='12345567812341234', width=180)
            self.credit.place(relx = 1, x =-20, y = 125, anchor ='ne')
            
            self.name1 = customtkinter.CTkEntry(master=self.setup_transaction_frame, placeholder_text='name', width=180)
            self.name1.place(relx = 1, x =-20, y = 165, anchor ='ne')
            
            self.purpose = customtkinter.CTkEntry(master=self.setup_transaction_frame, placeholder_text='purpose', width=180)
            self.purpose.place(relx = 1, x =-20, y = 205, anchor ='ne')
            db.close()
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy()      
        
        
    def check_amount_inputs(self):
        credit = self.credit.get()
        amount_pay = self.amount1.get()
        debit = self.debit.get()
        name1 = self.name1.get()
        purpose = self.purpose.get()
        if credit == '':
            self.error_label.configure(text="Credit Account shouldn't be empty")
        elif credit == debit:
            self.error_label.configure(text="Self Transactions is not allowed!!")
        elif len(credit) != 16:
            self.error_label.configure(text="Credit Account length should be 16")
        elif check_pay(credit, amount_pay, debit, name1, purpose, self.email, self.balance):
            message = f"A new Transaction was made from your account to account {credit} \n\n previous balance: {self.balance} and the new balance {int(self.balance) - int(amount_pay)} \n\n this is for {purpose}"
            send_mail_transaction(self.email, message)
            messagebox.showinfo("Success", "Deposit was made successfully")
            self.master.destroy()
        else:
            self.error_label.configure(text="Check the Payment details")
            
            
    def close(self):
        self.master.destroy()
            
            
class AddAccountDetailsFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_account_frame()
        
    def setup_account_frame(self):
        self.setup_account_frame = customtkinter.CTkFrame(master=self, width=450, height=450, corner_radius=24, bg_color="transparent")
        self.setup_account_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.account = customtkinter.CTkLabel(master=self.setup_account_frame, text="Account Details",
                                           text_color='red', font=('Times Romans', 14))
        self.account.place(x=20, y=20, anchor="w")
        self.error_label = customtkinter.CTkLabel(master=self.setup_account_frame, text="", font=('Century Gothic', 12), text_color="red")
        self.error_label.place(x=20, y=25)
        self.email = customtkinter.CTkLabel(master=self.setup_account_frame, text="Email Address: ",
                                           text_color='red', font=('Times Romans', 14))
        self.email.place(x=20, y=60, anchor="w")
        self.number = customtkinter.CTkLabel(master=self.setup_account_frame, text="Account Number: ",
                                           text_color='green', font=('Times Romans', 14))
        self.number.place(x=20, y=100, anchor="w")
        self.balance = customtkinter.CTkLabel(master=self.setup_account_frame, text="Online Working Balance: ",
                                           text_color='green', font=('Times Romans', 14))
        self.balance.place(x=20, y=140, anchor="w")
        self.phone = customtkinter.CTkLabel(master=self.setup_account_frame, text="Phone Number: ",
                                           text_color='green', font=('Times Romans', 14))
        self.phone.place(x=20, y=180, anchor="w")
        self.name = customtkinter.CTkLabel(master=self.setup_account_frame, text="User Name: ",
                                           text_color='green', font=('Times Romans', 14))
        self.name.place(x=20, y=220, anchor="w")
        self.type = customtkinter.CTkLabel(master=self.setup_account_frame, text="Account Type: ",
                                           text_color='green', font=('Times Romans', 14))
        self.type.place(x=20, y=260, anchor="w")
        self.view_button = customtkinter.CTkButton(master=self.setup_account_frame, 
                                                   hover_color='green', text="SAVE", width=150
                                                   , command=self.check_account_details)
        self.view_button.place(x =20, y = 300)
        self.view_button = customtkinter.CTkButton(master=self.setup_account_frame, 
                                                   hover_color='red', text="CLOSE", width=150, command=self.close_profile)
        self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
        self.email1 = customtkinter.CTkEntry(master=self.setup_account_frame,
                                           text_color='black', font=('Times Romans', 14))
        self.email1.insert(0, self.usermail)
        self.email1.configure(state="disabled")
        self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
        
        self.number1 = customtkinter.CTkEntry(master=self.setup_account_frame, placeholder_text="Account Number: ",
                                           text_color='black', font=('Times Romans', 14))
        self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
        self.balance1 = customtkinter.CTkEntry(master=self.setup_account_frame, placeholder_text="Online Working Balance: ",
                                           text_color='black', font=('Times Romans', 14))
        self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
        self.phone1 = customtkinter.CTkEntry(master=self.setup_account_frame, placeholder_text="Phone Number: ",
                                           text_color='black', font=('Times Romans', 14))
        self.phone1.place(relx = 1, x =-2, y=180, anchor ='ne')
        self.name1 = customtkinter.CTkEntry(master=self.setup_account_frame, placeholder_text="User Name: ",
                                           text_color='black', font=('Times Romans', 14))
        self.name1.place(relx = 1, x =-2, y=220, anchor ='ne')
        self.type1 = customtkinter.CTkEntry(master=self.setup_account_frame, placeholder_text="Account Type: ",
                                           text_color='black', font=('Times Romans', 14))
        self.type1.place(relx = 1, x =-2, y=260, anchor ='ne')
        
        
    def check_account_details(self):
        email = self.email1.get()
        account = self.number1.get()
        balance =self.balance1.get()
        name = self.name1.get()
        phone = self.phone1.get()
        acc_type = self.type1.get()
        if not email or not account or not balance or not phone or not name or not acc_type:
            self.error_label.configure(text="Error: All fields must be filled.")
        elif len(account) != 16:
            self.error_label.configure(text="Error: Account number must be exactly 16 characters.")
        elif add_account(email, account, balance, name, phone, acc_type):
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Email address already exists.")
            
    def close_profile(self):
        self.master.destroy()
        
        
class AddNewDepositFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_deposit_frame()
        
    def setup_deposit_frame(self):
        db, cursor = get_database_connection()
        
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            cursor.execute(query, (self.usermail,))
            data = cursor.fetchall()
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Deposit",
                                            text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                            text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Number: ",
                                            text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Online Working Balance: ",
                                            text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Deposit Amount: ",
                                            text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=180, anchor="w")
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                    hover_color='green', text="SAVE", width=150,
                                                    command=self.add_deposit)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                    hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                            text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
            
            self.number1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Account Number: ",
                                            text_color='black', font=('Times Romans', 14))
            for row in data:
                account_id = row[0]
            self.number1.insert(0, account_id)
            self.number1.configure(state="disabled")
            self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
            
            self.balance1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Online Working Balance: ",
                                            text_color='black', font=('Times Romans', 14))
            for row in data:
                balance = row[1]
            
            self.balance1.insert(0, balance)
            for row in data:
                name = row[2]
            self.name_ben = name
            self.balance1.configure(state="disabled")
            self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.deposit1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Deposit Amount: ",
                                            text_color='black', font=('Times Romans', 14))
            self.deposit1.place(relx = 1, x =-2, y=180, anchor ='ne')
            db.close() 
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy()     
        
        
    def add_deposit(self):
        email = self.email1.get()
        account = self.number1.get()
        balance =self.balance1.get()
        deposit = self.deposit1.get()
        if deposit == '':
            messagebox.showerror("Error", "Please input the amount to deposit")
        elif int(deposit) < 100:
            messagebox.showerror("Error", "You are allowed to deposit more than 100 only!!")
        elif deposit_transaction(email, account, balance, deposit, self.name_ben):
            message = f"A new Deposit was made previus balance: {balance} and the new balance {int(balance) + int(deposit)}"
            send_mail_transaction(email, message)
            messagebox.showinfo("Success", "Deposit was made successfully")
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
            
            
class AddAccountWithdrawalFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_deposit_frame()
        
    def setup_deposit_frame(self):
        db, cursor = get_database_connection()
        
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            cursor.execute(query, (self.usermail,))
            data = cursor.fetchall()
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Withdrawal",
                                            text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                            text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Number: ",
                                            text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Online Working Balance: ",
                                            text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Withdrawal Amount: ",
                                            text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=180, anchor="w")
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                    hover_color='green', text="WithDraw", width=150,
                                                    command=self.add_deposit)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                    hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                            text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
            
            self.number1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Account Number: ",
                                            text_color='black', font=('Times Romans', 14))
            for row in data:
                account_id = row[0]
            self.number1.insert(0, account_id)
            self.number1.configure(state="disabled")
            self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
            
            self.balance1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Online Working Balance: ",
                                            text_color='black', font=('Times Romans', 14))
            for row in data:
                balance = row[1]
            
            self.balance1.insert(0, balance)
            for row in data:
                name = row[2]
            self.name_ben = name
            self.balance1.configure(state="disabled")
            self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.deposit1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="WithDrawal Amount: ",
                                            text_color='black', font=('Times Romans', 14))
            self.deposit1.place(relx = 1, x =-2, y=180, anchor ='ne')
            db.close() 
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy()      
        
        
    def add_deposit(self):
        email = self.email1.get()
        account = self.number1.get()
        balance =self.balance1.get()
        deposit = self.deposit1.get()
        if deposit == '':
            messagebox.showerror("Error", "Please input the amount to deposit")
        elif int(deposit) < 100:
            messagebox.showerror("Error", "You are allowed to Withdraw amount less than 100 only!!")
        elif int(deposit) > int(balance):
            messagebox.showerror("Error", "You are allowed to Withdraw amount more than the balance!!!")
        elif withdrawal_transaction(email, account, balance, deposit, self.name_ben):
            message = f"A new Withdrawal was made previus balance: {balance} and the new balance {int(balance) - int(deposit)}"
            send_mail_transaction(email, message)
            messagebox.showinfo("Success", "Withdrawal was made successfully")
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
            
            
class AddNewVisualizeFrame(customtkinter.CTkFrame):
    def __init__(self, visualize, emaildb):
        super().__init__(visualize)
        self.visualize = visualize
        self.usermail=emaildb
        self.setup_visualize_frame()
        
    def setup_visualize_frame(self):
        self.master.change_geometry("1280x720")
        self.master.change_title("Visualization page")
        self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=1200, height=700, corner_radius=24, bg_color="transparent")
        self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.action_part = customtkinter.CTkFrame(master=self.setup_deposit_frame, width=300, height=400, corner_radius=24, bg_color="green")
        self.action_part.place(relx = 1, x =-20, y = 60, anchor='ne')  
        customtkinter.CTkLabel(master=self.action_part, text="CHOOSE AN ACTION: ", text_color='red', font=('Arial', 15, 'bold'), padx=20).place(relx = 1, x =-20, y = 60, anchor='e')
        self.new_txn_button = customtkinter.CTkButton(master=self.action_part, 
                                                      hover_color='pink', text="Monthly Transactions", width=240, command=self.monthly)
        self.new_txn_button.place(x =20, y = 100)

        self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
                                                        hover_color='blue', text="Deposit Vs WithDrawals", width=240, command=self.DepVsWith)
        self.visualize_button.place(x =20, y = 150)        
        
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='red', text="Deposits", width=240, command=self.Dep)
        self.view_button.place(x =20, y = 200)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='red', text="WithDraws", width=240, command=self.Withdraw)
        self.view_button.place(x =20, y = 250)
        self.view_button = customtkinter.CTkButton(master=self.action_part, 
                                                   hover_color='green', text="Others", width=240, command=self.Other)
        self.view_button.place(x =20, y = 300)
        self.back_button = customtkinter.CTkButton(
            master=self,
            width=30,
            height=30,
            text="◀️", 
            corner_radius=6,
            fg_color="#72bcd4",
            text_color="#1e5364",
            hover_color="#e8f4f8",
            command=self.master.open_main_frame
        )
        self.back_button.place(x =20, y = 350)
        self.frame = customtkinter.CTkFrame(master=self.setup_deposit_frame, width=500, height=600, corner_radius=24, bg_color="green")
        self.frame.place(x =100, y = 10)
        
        db, cursor = get_database_connection()
        
        query = '''
            SELECT Purpose, SUM(Amount) as total
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = ? and email = ?
            GROUP BY Purpose
        '''
        current_month = datetime.now().strftime("%Y-%m")
        df = pd.read_sql_query(query, db, params=(current_month, self.usermail,))
        fig = Figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        if not df.empty:
            df.plot.pie(
                y="total",
                labels=df["Purpose"],
                autopct='%1.1f%%',
                ax=ax,
                legend=False,
                startangle=90
            )
            ax.set_ylabel("") 
            ax.set_title("Monthly Transactions by Purpose")
            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            messagebox.showerror("Error", "No transactions for the current month.")
        db.close()
        
    def monthly(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        db, cursor = get_database_connection()
        
        query = '''
            SELECT Purpose, SUM(Amount) as total
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = ? and email = ?
            GROUP BY Purpose
        '''
        current_month = datetime.now().strftime("%Y-%m")
        df = pd.read_sql_query(query, db, params=(current_month, self.usermail,))
        fig = Figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        if not df.empty:
            df.plot.pie(
                y="total",
                labels=df["Purpose"],
                autopct='%1.1f%%',
                ax=ax,
                legend=False,
                startangle=90
            )
            ax.set_ylabel("") 
            ax.set_title("Monthly Transactions by Purpose")
            
            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            messagebox.showerror("Error", "No transactions for the current month.")
        db.close()
        
    def DepVsWith(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        db, cursor = get_database_connection()
        
        query = '''
            SELECT 
                CASE 
                    WHEN Purpose LIKE '%deposit%' THEN 'Deposit'
                    WHEN Purpose LIKE '%withdraw%' THEN 'Withdrawal'
                    ELSE 'Other'
                END as TransactionType,
                SUM(Amount) as total
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = strftime('%Y-%m', 'now')
            AND email = ?
            GROUP BY TransactionType
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        db.close()
        df = pd.DataFrame(data, columns=['TransactionType', 'total'])
        df = df[df['TransactionType'].isin(['Deposit', 'Withdrawal'])]
        
        fig = Figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        
        if not df.empty:

            df.plot.bar(x='TransactionType', y='total', ax=ax, color=['green', 'red'], legend=False)

            ax.set_title('Deposits vs Withdrawals')
            ax.set_ylabel('Total Amount')
            ax.set_xlabel('Transaction Type')
            for label in ax.get_xticklabels():
                label.set_rotation(45)
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
            
        else:
            messagebox.showerror("Error", "No withdrawals nor deposits for the current month.")
        
    def Dep(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        db, cursor = get_database_connection()
        query = '''
            SELECT strftime('%d', Timestamp) as Day, SUM(Amount) as Total
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = ? AND email = ? AND Purpose LIKE '%deposit%'
            GROUP BY strftime('%d', Timestamp)
            ORDER BY strftime('%d', Timestamp)
        '''
        current_month = datetime.now().strftime("%Y-%m")
        df = pd.read_sql_query(query, db, params=(current_month, self.usermail))
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        if not df.empty:
            ax.plot(df['Day'], df['Total'], marker='o', color='green', label='Deposits')
            ax.set_title("Daily Deposits for the Current Month")
            ax.set_xlabel("Day of the Month")
            ax.set_ylabel("Total Deposits")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.legend()
            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            messagebox.showerror("Error", "No deposits for the current month.")

        db.close()
        
    def Withdraw(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        db, cursor = get_database_connection()
        query = '''
            SELECT strftime('%d', Timestamp) as Day, SUM(Amount) as Total
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = ? AND email = ? AND Purpose LIKE '%withdrawal%'
            GROUP BY strftime('%d', Timestamp)
            ORDER BY strftime('%d', Timestamp)
        '''
        current_month = datetime.now().strftime("%Y-%m")
        df = pd.read_sql_query(query, db, params=(current_month, self.usermail))
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        if not df.empty:
            ax.plot(df['Day'], df['Total'], marker='o', color='red', label='Withdraw')
            ax.set_title("Daily Withdraw for the Current Month")
            ax.set_xlabel("Day of the Month")
            ax.set_ylabel("Total Withdrawals")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.legend()
            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            messagebox.showerror("Error", "No withdrawals for the current month.")

        db.close()
        
   

    def Other(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        db, cursor = get_database_connection()
        query = '''
            SELECT strftime('%d', Timestamp) as Day, SUM(Amount) as Total, Purpose
            FROM Transactions
            WHERE strftime('%Y-%m', Timestamp) = ? 
            AND email = ? 
            AND NOT Purpose LIKE '%withdrawal%' 
            AND NOT Purpose LIKE '%deposit%'
            GROUP BY strftime('%d', Timestamp), Purpose
            ORDER BY strftime('%d', Timestamp)
        '''
        current_month = datetime.now().strftime("%Y-%m")
        df = pd.read_sql_query(query, db, params=(current_month, self.usermail))
        db.close()

        print(df.head()) 
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        if not df.empty:
            unique_purposes = df['Purpose'].unique()
            cmap = get_cmap("tab10")  
            colors = {purpose: cmap(i / len(unique_purposes)) for i, purpose in enumerate(unique_purposes)}
            for purpose, group in df.groupby('Purpose'):
                ax.plot(group['Day'], group['Total'], marker='o', label=purpose, color=colors[purpose])

            ax.set_title("Daily Other Transactions for the Current Month")
            ax.set_xlabel("Day of the Month")
            ax.set_ylabel("Total Amount")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.legend(title="Purpose")
            canvas = FigureCanvasTkAgg(fig, self.frame)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            canvas.draw()
        else:
            messagebox.showerror("Error", "No other transactions for the current month.")

        
    # def open_main_frame(self):
    #     if self.visualize.winfo_exists():
    #         self.visualize.withdraw()  
    #         self.master.deiconify()  
    #         self.master.open_loggedin_frame(self.usermail)  
    #     else:
    #         print(self.visualize.winfo_exists)
            
            
class AddNewBudgetFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_visualize_frame()
        
    def setup_visualize_frame(self):
        self.master.change_geometry("1280x720")
        self.master.change_title("Plan Window")
        self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=1200, height=700, corner_radius=24, bg_color="transparent")
        self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.action_part = customtkinter.CTkFrame(master=self.setup_deposit_frame, width=300, height=400, corner_radius=24, bg_color="green")
        self.action_part.place(relx = 1, x =-20, y = 60, anchor='ne')
        customtkinter.CTkLabel(master=self.action_part, text="CHOOSE AN ACTION: ", text_color='red', font=('Arial', 15, 'bold'), padx=20).place(relx = 1, x =-20, y = 60, anchor='e')
        self.new_txn_button = customtkinter.CTkButton(master=self.action_part, 
                                                      hover_color='pink', text="Monthly Budget", width=240, command=self.budget)
        self.new_txn_button.place(x =20, y = 100)

        self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
                                                        hover_color='blue', text="Investment", width=240, command=self.invest)
        self.visualize_button.place(x =20, y = 150) 
        self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
                                                        hover_color='blue', text="Assets and Stock", width=240, command=self.assets)
        self.visualize_button.place(x =20, y = 200)
        # self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
        #                                                 hover_color='blue', text="Pontenial Taxes", width=240)
        # self.visualize_button.place(x =20, y = 250)
        self.visualize_button = customtkinter.CTkButton(master=self.action_part, 
                                                        hover_color='blue', text="Group", width=240, command=self.groups)
        self.visualize_button.place(x =20, y = 250)
        
        self.create_buttons()
        
        self.db, self.cursor = get_database_connection()
        
        self.budget_frame = customtkinter.CTkFrame(master=self.setup_deposit_frame, width=1000, height=700, corner_radius=24, bg_color="lightblue")
        self.budget_frame.place(x=30, y=60, anchor='nw')
        customtkinter.CTkLabel(master=self.budget_frame, text="Budget Table", text_color='black', font=('Arial', 18, 'bold')).place(relx=0.5, y=10, anchor='n')

        self.tree = ttk.Treeview(self.budget_frame, height=15)
        self.update_treeview_headers(data_type="budget")

        self.tree.pack(pady=50, padx=20)

        self.load_budget()
        self.tree.bind("<Double-1>", self.edit_cell)
        
    def update_treeview_headers(self, data_type="budget"):
        self.tree["columns"] = []
        self.tree["show"] = "headings"
        if data_type == "budget":
            self.tree["columns"] = ("email", "amount", "purpose", "current_expenses", "group_in")
            self.tree.heading("email", text="Email")
            self.tree.heading("amount", text="Amount")
            self.tree.heading("purpose", text="Purpose")
            self.tree.heading("current_expenses", text="Current Expenses")
            self.tree.heading("group_in", text="Group")
            
            self.tree.column("email", anchor='center', width=150)
            self.tree.column("amount", anchor='center', width=150)
            self.tree.column("purpose", anchor='center', width=150)
            self.tree.column("current_expenses", anchor='center', width=150)
            self.tree.column("group_in", anchor='center', width=100)
            
        elif data_type == "investment":
            self.tree["columns"] = ("email", "amount", "purpose", "years_invested")
            self.tree.heading("email", text="Email")
            self.tree.heading("amount", text="Amount")
            self.tree.heading("purpose", text="Purpose")
            self.tree.heading("years_invested", text="Years Invested")
            
            self.tree.column("email", anchor='center', width=150)
            self.tree.column("amount", anchor='center', width=150)
            self.tree.column("purpose", anchor='center', width=150)
            self.tree.column("years_invested", anchor='center', width=150)
            
        elif data_type == "assets":
            self.tree["columns"] = ("Email", "Asset_Type", "Asset_name", "Asset_Amount")
            self.tree.heading("Email", text="Email")
            self.tree.heading("Asset_Type", text="Asset Type")
            self.tree.heading("Asset_name", text="Asset name")
            self.tree.heading("Asset_Amount", text="Asset Amount")
            
            self.tree.column("Email", anchor='center', width=150)
            self.tree.column("Asset_Type", anchor='center', width=150)
            self.tree.column("Asset_name", anchor='center', width=150)
            self.tree.column("Asset_Amount", anchor='center', width=150)
            
        elif data_type=="groups":
            self.tree["columns"] = ("email", "amount", "purpose", "current_expenses", "group_in")
            self.tree.heading("email", text="Email")
            self.tree.heading("amount", text="Amount")
            self.tree.heading("purpose", text="Purpose")
            self.tree.heading("current_expenses", text="Current Expenses")
            self.tree.heading("group_in", text="Group")
            
            self.tree.column("email", anchor='center', width=150)
            self.tree.column("amount", anchor='center', width=150)
            self.tree.column("purpose", anchor='center', width=150)
            self.tree.column("current_expenses", anchor='center', width=150)
            self.tree.column("group_in", anchor='center', width=100)
        
    def create_buttons(self):
        buttons = [
            ("Monthly Budget", self.view_monthly_budget),
            ("Investment", self.view_investment_budget),
            # ("Potential Taxes"),
            ("Assets", self.view_assets),
            ("Groups", self.view_groups),
            ("Back", self.master.open_main_frame)
        ]

        button_width = 20  
        for idx, (text, command) in enumerate(buttons):
            button = customtkinter.CTkButton(
                master=self.setup_deposit_frame, text=text, command=command, width=button_width * 5
            )
            button.place(x=30 + (button_width * 5 + 10) * idx, y=10)  


    def load_budget(self):
        self.update_treeview_headers(data_type="budget")
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute(
            "SELECT id, email, amount, purpose, current_expenses, group_in FROM budget WHERE email = ?", 
            (self.usermail,)
        )
        rows = self.cursor.fetchall()
        
        total_amount = 0
        total_expenses = 0

        for row in rows:
            id_, email, amount, purpose, current_expenses, group_in = row
            
            
            if current_expenses is None:
                current_expenses = 0.0
                
            self.tree.insert("", "end", iid=id_, values=(email, amount, purpose, current_expenses, group_in))
            total_amount += float(amount)
            total_expenses += float(current_expenses)
            
        self.tree.insert(
            "", "end", iid="totals", 
            values=("TOTALS", total_amount, "-", total_expenses, "-", "-"),
            tags=("totals",)
        )
        self.tree.tag_configure("totals", background="lightgray", font=("Arial", 10, "bold"))


    def edit_cell(self, event):
        selected_item = self.tree.selection()[0]
        if selected_item == "totals":
            return
        col_id = self.tree.identify_column(event.x)  
        col_num = int(col_id.replace("#", "")) - 1  

        if col_num == 3:  
            item_values = self.tree.item(selected_item, "values")
            old_value = item_values[col_num]

            entry = ttk.Entry(self.tree, width=15)
            entry.insert(0, old_value)
            entry.place(x=event.x, y=event.y)

            def save_edit(event=None):
                new_value = entry.get()
                self.tree.item(selected_item, values=(*item_values[:col_num], new_value, *item_values[col_num + 1:]))
                entry.destroy()           

                self.cursor.execute(
                    "UPDATE budget SET current_expenses = ? WHERE id = ?", 
                    (float(new_value) + float(old_value), selected_item)
                )
                self.db.commit()
                messagebox.showerror("Success", "Current Expenses updated")

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", lambda e: entry.destroy())
            
    def load_investment(self):
        self.update_treeview_headers(data_type="investment")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute(
            "SELECT id, email, amount, purpose, years_invested FROM Investment WHERE email = ?", 
            (self.usermail,)
        )
        rows = self.cursor.fetchall()
        
        total_amount = 0
        if rows:
            for row in rows:
                id_, email, amount, purpose, years_invested = row
                self.tree.insert("", "end", iid=id_, values=(email, amount, purpose, years_invested))
                total_amount += float(amount)
            self.tree.insert(
            "", "end", iid="totals", 
            values=("TOTALS", total_amount, "-", "-"),
            tags=("totals",))
            self.tree.tag_configure("totals", background="lightgray", font=("Arial", 10, "bold"))
            
    def load_assets(self):
        self.update_treeview_headers(data_type="assets")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute(
            "SELECT id, Email, Asset_Type, Asset_name, Asset_Amount FROM Assets WHERE email = ?", 
            (self.usermail,)
        )
        rows = self.cursor.fetchall()
        
        total_amount = 0
        if rows:
            for row in rows:
                id_, Email, Asset_Amount, Asset_Type,  Asset_name = row
                self.tree.insert("", "end", iid=id_, values=(Email, Asset_Type, Asset_name, Asset_Amount))
                if Asset_Amount is None:
                    Asset_Amount = 0
                total_amount += float(Asset_Amount)
            self.tree.insert(
            "", "end", iid="totals", 
            values=("TOTALS", "-", "-", total_amount),
            tags=("totals",))
            self.tree.tag_configure("totals", background="lightgray", font=("Arial", 10, "bold"))
            
    def load_groups(self):
        self.update_treeview_headers(data_type="groups")
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = '''
            SELECT group_in
            FROM budget
            WHERE Email = ?
        '''
        self.cursor.execute(query, (self.usermail,))
        data = self.cursor.fetchone()
        
        if data:
            self.cursor.execute(
                "SELECT id, email, amount, purpose, current_expenses, group_in FROM budget WHERE group_in = ?", 
                (data[0],)
            )
            rows = self.cursor.fetchall()

            for row in rows:
                id_, email, amount, purpose, current_expenses, group_in = row       
                self.tree.insert("", "end", iid=id_, values=(email, amount, purpose, current_expenses, group_in))
                
            if data[0] is not None: 
                separated_strings = data[0].split(';')
                for group_name in separated_strings:
                    self.cursor.execute(
                        "SELECT Total_members FROM BGroup WHERE Email=? AND Group_Name=?", 
                        (self.usermail, group_name)
                    )
                    print(group_name)
                    data1 = self.cursor.fetchone()
                    if data1:
                        self.tree.insert(
                            "", "end", iid=f"totals_{group_name}",  
                            values=(f"TOTALS Members ({group_name})", "-", "-", data1[0], "-", "-"),
                            tags=("totals",)
                        )
                        print(separated_strings)
                        self.tree.tag_configure("totals", background="lightgray", font=("Arial", 10, "bold"))
            else:
                print("No group created")
                        
        
        
    def view_monthly_budget(self):
        print("View Monthly Budget")        
        self.load_budget()
        
    def view_investment_budget(self):
        print("View Investments Budget")
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Investment (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Account TEXT,
                        Balance INTEGER,
                        Purpose TEXT,
                        Amount TEXT,
                        Years_Invested TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
            print("Table created")
            db.commit()
            self.load_investment()
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
             
             
    def view_assets(self):
        print("View Assets")
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Assets (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Account TEXT,
                        Balance INTEGER,
                        Asset_Type TEXT,
                        Asset_name TEXT,
                        Asset_Amount TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
            print("Table created")
            db.commit()
            self.load_assets()
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
             
    def view_groups(self):
        print("View Group Work")
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS BGroup (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Group_Name TEXT,
                        Group_Purpose TEXT,
                        Group_members TEXT,
                        Total_members TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
            cursor.execute(
                "SELECT Group_Name, Group_members FROM BGroup WHERE Group_members LIKE ?",
                (f"%{self.usermail}%",)
            )
            data1 = cursor.fetchall()
            if data1:
                group_members_combined = ";".join([row[0] for row in data1 if row[0]])
                cursor.execute("UPDATE budget SET Group_IN = ? WHERE Email = ?", (group_members_combined, self.usermail))
                db.commit()
            
            
            
            self.load_groups()
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
        
        
    
    
    
    def budget(self):
        self.master.add_budget_details(self.usermail)
        
    def invest(self):
        self.master.add_invest_details(self.usermail)
        
    def assets(self):
        self.master.add_assets_details(self.usermail)
        
    def groups(self):
        self.master.add_groups_details(self.usermail)
        

        
        
class AddNewMbudgetFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_budget_frame()
        
    def setup_budget_frame(self):
        db, cursor = get_database_connection()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Budget (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Email TEXT,
                    Account TEXT,
                    Balance INTEGER,
                    Purpose TEXT,
                    Amount TEXT,
                    Current_Expenses TEXT,
                    Group_IN TEXT NULLABLE,
                    TIMESTAMP TIMESTAMP
                )
            ''')
            
            
            db.commit()
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table") 
        
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Budget Plan",
                                                text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                                text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Number: ",
                                                text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Online Working Balance: ",
                                                text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.budget = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Monthly Budget Amount: ",
                                                text_color='green', font=('Times Romans', 14))
            self.budget.place(x=20, y=180, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Purpose: ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=220, anchor="w")
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='green', text="Save", width=150,
                                                        command=self.budget_save)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                                text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
                
            self.number1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Account Number: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                account_id = row[0]
            self.number1.insert(0, account_id)
            self.number1.configure(state="disabled")
            self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
                
            self.balance1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Online Working Balance: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                balance = row[1]
                
            self.balance1.insert(0, balance)
            for row in data:
                name = row[2]
            self.name_ben = name
            self.balance1.configure(state="disabled")
            self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.amount = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Amount ",
                                                text_color='black', font=('Times Romans', 14))
            self.amount.place(relx = 1, x =-2, y=180, anchor ='ne')
            self.purpose = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="purpose ",
                                                text_color='black', font=('Times Romans', 14))
            self.purpose.place(relx = 1, x =-2, y=220, anchor ='ne')
            
            
            
            
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy() 
            
    def budget_save(self):
        email1 = self.email1.get()
        number1 = self.number1.get()
        amount = self.amount.get()
        purpose = self.purpose.get()
        balance = self.balance1.get()
        
        if not purpose or not amount:
            messagebox.showerror("Error", "Please enter the amount and the Purpose")
        else:
            save_budget(email1, number1, balance, amount, purpose)
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
            
            
class AddNewMInvestFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_budget_frame()
        
    def setup_budget_frame(self):
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Investment (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Account TEXT,
                        Balance INTEGER,
                        Purpose TEXT,
                        Amount TEXT,
                        Years_Invested TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
            print("Table created")
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Investment Plan",
                                                text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                                text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Number: ",
                                                text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Online Working Balance: ",
                                                text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.budget = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Investment Amount: ",
                                                text_color='green', font=('Times Romans', 14))
            self.budget.place(x=20, y=180, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Purpose: ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=220, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Years: ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=260, anchor="w")
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='green', text="Save", width=150,
                                                        command=self.investment_save)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                                text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
                
            self.number1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Account Number: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                account_id = row[0]
            self.number1.insert(0, account_id)
            self.number1.configure(state="disabled")
            self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
                
            self.balance1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Online Working Balance: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                balance = row[1]
                
            self.balance1.insert(0, balance)
            for row in data:
                name = row[2]
            self.name_ben = name
            self.balance1.configure(state="disabled")
            self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.amount = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Amount ",
                                                text_color='black', font=('Times Romans', 14))
            self.amount.place(relx = 1, x =-2, y=180, anchor ='ne')
            self.purpose = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="purpose ",
                                                text_color='black', font=('Times Romans', 14))
            self.purpose.place(relx = 1, x =-2, y=220, anchor ='ne')
            self.years= customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Years of investment ",
                                                text_color='black', font=('Times Romans', 14))
            self.years.place(relx = 1, x =-2, y=260, anchor ='ne')
            
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy() 
        db.close()
            
    def investment_save(self):
        email1 = self.email1.get()
        number1 = self.number1.get()
        amount = self.amount.get()
        purpose = self.purpose.get()
        balance = self.balance1.get()
        years = self.years.get()
        
        if not purpose or not amount or not years:
            messagebox.showerror("Error", "Please enter the amount and the Purpose")
        else:
            save_invest(email1, number1, balance, amount, purpose, years)
            messagebox.showinfo("Success", "Records inserted successfully")
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
            
            
class AddNewMAssetsFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_budget_frame()
        
    def setup_budget_frame(self):
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Assets (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Account TEXT,
                        Balance INTEGER,
                        Asset_Type TEXT,
                        Asset_name TEXT,
                        Asset_Amount TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
            print("Table created")
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Investment Plan",
                                                text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                                text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Account Number: ",
                                                text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Online Working Balance: ",
                                                text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.budget = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Asset Type: ",
                                                text_color='green', font=('Times Romans', 14))
            self.budget.place(x=20, y=180, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Asset name: ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=220, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Asset Amount: ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=260, anchor="w")
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='green', text="Save", width=150,
                                                        command=self.investment_save)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                                text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
                
            self.number1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Account Number: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                account_id = row[0]
            self.number1.insert(0, account_id)
            self.number1.configure(state="disabled")
            self.number1.place(relx = 1, x =-2, y=100, anchor ='ne')
                
            self.balance1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Online Working Balance: ",
                                                text_color='black', font=('Times Romans', 14))
            for row in data:
                balance = row[1]
                
            self.balance1.insert(0, balance)
            for row in data:
                name = row[2]
            self.name_ben = name
            self.balance1.configure(state="disabled")
            self.balance1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.atype = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Asset type ",
                                                text_color='black', font=('Times Romans', 14))
            self.atype.place(relx = 1, x =-2, y=180, anchor ='ne')
            self.aname = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Asset Name ",
                                                text_color='black', font=('Times Romans', 14))
            self.aname.place(relx = 1, x =-2, y=220, anchor ='ne')
            self.amount= customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Asset Amount ",
                                                text_color='black', font=('Times Romans', 14))
            self.amount.place(relx = 1, x =-2, y=260, anchor ='ne')
            
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy() 
        db.close()
            
    def investment_save(self):
        email1 = self.email1.get()
        number1 = self.number1.get()
        balance = self.balance1.get()
        atype = self.atype.get()
        aname = self.aname.get()
        amount = self.amount.get()
        
        if not atype or not aname or not amount:
            messagebox.showerror("Error", "Please enter the amount and the asset type")
        else:
            save_asset(email1, number1, balance, atype, aname, amount)
            messagebox.showinfo("Success", "Records inserted successfully")
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
            
class AddNewMGroupFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_budget_frame()
        
    def setup_budget_frame(self):
        db, cursor = get_database_connection()
        try:
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS BGroup (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Email TEXT,
                        Group_Name TEXT,
                        Group_Purpose TEXT,
                        Group_members TEXT,
                        Total_members TEXT,
                        TIMESTAMP TIMESTAMP
                    )
                ''')
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Investment Plan",
                                                text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                                text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Group Name: ",
                                                text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
            self.balance = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Group Purpose: ",
                                                text_color='green', font=('Times Romans', 14))
            self.balance.place(x=20, y=140, anchor="w")
            self.purpose = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Group Members \n(Select from the dropdwon below): ",
                                                text_color='green', font=('Times Romans', 14))
            self.purpose.place(x=20, y=180, anchor="w")
           
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='green', text="Save", width=150,
                                                        command=self.group_save)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                                text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
            
            self.atype = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Group Name ",
                                                text_color='black', font=('Times Romans', 14))
            self.atype.place(relx = 1, x =-2, y=100, anchor ='ne')
            self.purpose1 = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Group Purpose ",
                                                text_color='black', font=('Times Romans', 14))
            self.purpose1.place(relx = 1, x =-2, y=140, anchor ='ne')
            self.aname = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="Group Members",
                                  text_color='black', font=('Times Roman', 14))
            self.aname.place(relx = 1, x =-2, y=180, anchor ='ne')
            self.email_dropdown = customtkinter.CTkOptionMenu(master=self.setup_deposit_frame, values=["Select Emails"], 
                                                    font=("Arial", 12), command=self.update_selected_emails)
            self.email_dropdown.place(relx = 1, x =-2, y=220, anchor ='ne')
            self.load_emails()
            
            
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy() 
        db.close()
            
    def group_save(self):
        email1 = self.email1.get()
        atype = self.atype.get()
        purpose = self.purpose1.get()
        aname = self.aname.get()
        
        if not atype or not purpose:
            messagebox.showerror("Error", "Please provide the Group name and the group purpose")
        elif group_save(email1, atype, purpose, aname):
            messagebox.showinfo("Success", "Records saved successfully")
            self.master.destroy()
            
    def close(self):
        self.master.destroy()
        
    def load_emails(self):
        db, cursor = get_database_connection()
        cursor.execute("SELECT email FROM accounts")
        emails = cursor.fetchall()
        email_list = [email[0] for email in emails]  
        self.email_dropdown.configure(values=email_list)
        db.close()  
    
    def update_selected_emails(self, email):
        current_text = self.aname.get()
        if current_text == "":
            updated_text = email
        else:
            updated_text = f"{current_text}; {email}"
        self.aname.delete(0, "end")
        self.aname.insert(0, updated_text)
        
        
class AddNewMPasswordFrame(customtkinter.CTkFrame):
    def __init__(self, master, emaildb):
        super().__init__(master)
        self.master = master
        self.usermail=emaildb
        self.setup_budget_frame()
        
    def setup_budget_frame(self):
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
        except sqlite3.IntegrityError:
             messagebox.showerror("Error", "Unable To create the table")
        query = '''
            SELECT Account, Balance, name
            FROM Accounts
            WHERE Email = ?
        '''
        cursor.execute(query, (self.usermail,))
        data = cursor.fetchall()
        if data:
            self.setup_deposit_frame = customtkinter.CTkFrame(master=self, width=350, height=350, corner_radius=24, bg_color="transparent")
            self.setup_deposit_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            self.account = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Investment Plan",
                                                text_color='red', font=('Times Romans', 14))
            self.account.place(x=20, y=20, anchor="w")
            self.error_label = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="", font=('Century Gothic', 12), text_color="red")
            self.error_label.place(x=20, y=25)
            self.email = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="Email Address: ",
                                                text_color='green', font=('Times Romans', 14))
            self.email.place(x=20, y=60, anchor="w")
            self.number = customtkinter.CTkLabel(master=self.setup_deposit_frame, text="New Password: ",
                                                text_color='green', font=('Times Romans', 14))
            self.number.place(x=20, y=100, anchor="w")
           
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='green', text="Save", width=150,
                                                        command=self.password_save)
            self.view_button.place(x =20, y = 300)
            self.view_button = customtkinter.CTkButton(master=self.setup_deposit_frame, 
                                                        hover_color='red', text="CLOSE", width=150, command=self.close)
            self.view_button.place(relx = 1, x =-2, y = 300, anchor ='ne')
            self.email1 = customtkinter.CTkEntry(master=self.setup_deposit_frame,
                                                text_color='black', font=('Times Romans', 14))
            self.email1.insert(0, self.usermail)
            self.email1.configure(state="disabled")
            self.email1.place(relx = 1, x =-2, y=60, anchor ='ne')
            
            self.atype = customtkinter.CTkEntry(master=self.setup_deposit_frame, placeholder_text="New Password ",
                                                text_color='black', font=('Times Romans', 14), show="*")
            self.atype.place(relx = 1, x =-2, y=100, anchor ='ne')
            
        else:
            messagebox.showerror("Error", "Please create An Account with Us!!")
            self.master.destroy() 
        db.close()
    
    def password_save(self):
        email = self.email1.get()
        atype = self.atype.get()
        
        if not atype:
            messagebox.showerror("Error", "Please input the new password")
        elif password_save(email, atype):
            messagebox.showinfo("Success", "Password Updated successfully")
            self.master.destroy() 
        elif len(atype) < 8:
            messagebox.showerror("Error", "Please input password of length 8")
            
            
    def close(self):
        self.master.destroy()
        
        
            
    
