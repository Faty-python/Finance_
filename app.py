import tkinter
import customtkinter
from frames import AddAccountDetailsFrame, AddAccountWithdrawalFrame, AddNewBudgetFrame, AddNewDepositFrame, AddNewMAssetsFrame, AddNewMGroupFrame, AddNewMInvestFrame, AddNewMPasswordFrame, AddNewMbudgetFrame, AddNewVisualizeFrame, MainFrame, NewTransactionFrame, RegisterFrame, LoggedInFrame, ForgotPasswordFrame, ForgotPasswordFrame2

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class MainApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.title("Sign into your Account")
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both") 
        self.frames = {}

    def change_geometry(self, new_geometry):
        self.geometry(new_geometry)
    def change_title(self, new_title):
        self.title(new_title)

    def open_loggedin_frame(self, email):
        if hasattr(self, "main_frame") and self.main_frame.winfo_exists():
            self.main_frame.destroy()
        self.loggedin_frame = LoggedInFrame(self, email)
        self.frames["loggedin_frame"] = self.loggedin_frame
        self.loggedin_frame.pack(expand=True, fill="both") 

    def open_register_frame(self):
        self.main_frame.destroy()
        self.register_frame = RegisterFrame(self)
        self.frames["register_frame"] = self.register_frame
        self.register_frame.pack(expand=True, fill="both") 

    def open_forgot_password_frame(self):
        self.main_frame.destroy()
        self.main_frame = MainFrame(self)
        self.forgot_password_frame = ForgotPasswordFrame(self)
        self.frames["forgot_password_frame"] = self.forgot_password_frame
        self.forgot_password_frame.pack(expand=True, fill="both")

    def open_forgot_password_frame2(self, user_email):
        self.main_frame = MainFrame(self)
        self.forgot_password_frame2 = ForgotPasswordFrame2(self, user_email)
        self.frames["forgot_password_frame2"] = self.forgot_password_frame2
        self.forgot_password_frame2.pack(expand=True, fill="both")

    def open_main_frame(self):
        self.destroy_all_frames()
        self.change_title("Sign into your Account")
        self.main_frame = MainFrame(self)
        self.main_frame.pack(expand=True, fill="both")
        
        
    def open_master_frame(self, emaildb):
        self.destroy_all_frames()
        self.main_frame = LoggedInFrame(self, emaildb)
        self.main_frame.pack(expand=True, fill="both")
        
    def new_transaction(self, emaildb):
        #self.destroy_all_frames()
        self.new_transaction_window = customtkinter.CTkToplevel(self.master)
        self.new_transaction_window.title("New Transaction")  
        self.new_transaction_window.geometry("500x500")  
        self.new_transaction_window.resizable(False, False)  
        self.setup_transaction_frame = NewTransactionFrame(self.new_transaction_window, emaildb)
        self.frames['new_transaction'] = self.setup_transaction_frame
        self.setup_transaction_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_transaction_window.transient(self.master)
        self.new_transaction_window.grab_set()
        
    def add_account_details(self, emaildb):
        self.new_transaction_window = customtkinter.CTkToplevel(self.master)
        self.new_transaction_window.title("Account Details")  
        self.new_transaction_window.geometry("500x500")  
        self.new_transaction_window.resizable(False, False)
        self.setup_account_frame = AddAccountDetailsFrame(self.new_transaction_window, emaildb)
        self.frames['account_details'] = self.setup_account_frame
        self.setup_account_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_transaction_window.transient(self.master)
        self.new_transaction_window.grab_set()
        
        
    def add_new_withdrawal(self, emaildb):
        self.new_withdrawal_window = customtkinter.CTkToplevel(self.master)
        self.new_withdrawal_window.title("Account withdrawal")  
        self.new_withdrawal_window.geometry("500x500")  
        self.new_withdrawal_window.resizable(False, False)
        self.setup_withdrawal_frame = AddAccountWithdrawalFrame(self.new_withdrawal_window, emaildb)
        self.frames['account_withdrawal'] = self.setup_withdrawal_frame
        self.setup_withdrawal_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_withdrawal_window.transient(self.master)
        self.new_withdrawal_window.grab_set()
        
        
    def add_new_deposit(self, emaildb):
        self.new_deposit_window = customtkinter.CTkToplevel(self.master)
        self.new_deposit_window.title("ADD DEPOSITS")  
        self.new_deposit_window.geometry("400x400")  
        self.new_deposit_window.resizable(False, False)
        self.setup_deposit_frame = AddNewDepositFrame(self.new_deposit_window, emaildb)
        self.frames['account_deposit'] = self.setup_deposit_frame
        self.setup_deposit_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_deposit_window.transient(self.master)
        self.new_deposit_window.grab_set()
        
    def add_visualization(self, emaildb):
        self.visualize = AddNewVisualizeFrame(self, emaildb)
        self.frames["visualize"] = self.visualize
        self.visualize.pack(expand=True, fill="both")
        
    def add_budget(self, emaildb):
        self.budget = AddNewBudgetFrame(self, emaildb)
        self.frames["budget"] = self.budget
        self.budget.pack(expand=True, fill="both")
        
    def add_budget_details(self, emaildb):
        self.new_budget_window = customtkinter.CTkToplevel(self.master)
        self.new_budget_window.title("ADD BUDGET")  
        self.new_budget_window.geometry("400x400")  
        self.new_budget_window.resizable(False, False)
        self.setup_budget_frame = AddNewMbudgetFrame(self.new_budget_window, emaildb)
        self.frames['account_budget'] = self.setup_budget_frame
        self.setup_budget_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_budget_window.transient(self.master)
        self.new_budget_window.grab_set()
        
        
    def add_password_details(self, emaildb):
        self.new_budget_window = customtkinter.CTkToplevel(self.master)
        self.new_budget_window.title("Password Update")  
        self.new_budget_window.geometry("400x400")  
        self.new_budget_window.resizable(False, False)
        self.setup_budget_frame = AddNewMPasswordFrame(self.new_budget_window, emaildb)
        self.frames['account_budget'] = self.setup_budget_frame
        self.setup_budget_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_budget_window.transient(self.master)
        self.new_budget_window.grab_set()
        
    def add_invest_details(self, emaildb):
        self.new_budget_window = customtkinter.CTkToplevel(self.master)
        self.new_budget_window.title("ADD InvestMent")  
        self.new_budget_window.geometry("400x400")  
        self.new_budget_window.resizable(False, False)
        self.setup_budget_frame = AddNewMInvestFrame(self.new_budget_window, emaildb)
        self.frames['account_investment'] = self.setup_budget_frame
        self.setup_budget_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_budget_window.transient(self.master)
        self.new_budget_window.grab_set()
        
    def add_assets_details(self, emaildb):
        self.new_budget_window = customtkinter.CTkToplevel(self.master)
        self.new_budget_window.title("ADD Assests")  
        self.new_budget_window.geometry("400x400")  
        self.new_budget_window.resizable(False, False)
        self.setup_budget_frame = AddNewMAssetsFrame(self.new_budget_window, emaildb)
        self.frames['account_assets'] = self.setup_budget_frame
        self.setup_budget_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_budget_window.transient(self.master)
        self.new_budget_window.grab_set()
        
    def add_groups_details(self, emaildb):
        self.new_budget_window = customtkinter.CTkToplevel(self.master)
        self.new_budget_window.title("ADD Group")  
        self.new_budget_window.geometry("400x400")  
        self.new_budget_window.resizable(False, False)
        self.setup_budget_frame = AddNewMGroupFrame(self.new_budget_window, emaildb)
        self.frames['account_group'] = self.setup_budget_frame
        self.setup_budget_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.new_budget_window.transient(self.master)
        self.new_budget_window.grab_set()
        


    def destroy_all_frames(self):
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}  
        
    
