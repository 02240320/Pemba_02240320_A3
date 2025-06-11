import unittest
import random
from tkinter import Tk
from unittest.mock import patch, Mock

# Import the classes we need to test
from Pemba_02240320_A3_PA import (
    BankAccount,
    BankingGUI,
    InvalidInputError,
    InsufficientFundsError
)

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        """Set up test accounts before each test"""
        self.account1 = BankAccount("12345", "1234", "Personal", 1000)
        self.account2 = BankAccount("67890", "5678", "Business", 500)
  
    def test_initial_balance(self):
        """Test account initialization with correct balance"""
        self.assertEqual(self.account1.funds, 1000)
        self.assertEqual(self.account2.funds, 500)
    
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount"""
        self.assertTrue(self.account1.deposit(500))
        self.assertEqual(self.account1.funds, 1500)
    
    def test_deposit_negative_amount(self):
        """Test depositing a negative amount raises error"""
        with self.assertRaises(InvalidInputError):
            self.account1.deposit(-100)
    
    def test_deposit_zero_amount(self):
        """Test depositing zero raises error"""
        with self.assertRaises(InvalidInputError):
            self.account1.deposit(0)
    
    def test_withdraw_sufficient_funds(self):
        """Test withdrawing with sufficient funds"""
        self.assertTrue(self.account1.withdraw(500))
        self.assertEqual(self.account1.funds, 500)
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than balance"""
        with self.assertRaises(InsufficientFundsError):
            self.account1.withdraw(1500)
    
    def test_withdraw_negative_amount(self):
        """Test withdrawing negative amount"""
        with self.assertRaises(InvalidInputError):
            self.account1.withdraw(-100)
    
    def test_withdraw_zero_amount(self):
        """Test withdrawing zero"""
        with self.assertRaises(InvalidInputError):
            self.account1.withdraw(0)
    
    def test_transfer_successful(self):
        """Test successful transfer between accounts"""
        self.assertTrue(self.account1.transfer(300, self.account2))
        self.assertEqual(self.account1.funds, 700)
        self.assertEqual(self.account2.funds, 800)
    
    def test_transfer_insufficient_funds(self):
        """Test transfer with insufficient funds"""
        with self.assertRaises(InsufficientFundsError):
            self.account1.transfer(1500, self.account2)
    
    def test_mobile_topup_valid(self):
        """Test valid mobile top-up"""
        self.assertTrue(self.account1.mobile_topup(100, "77123456"))
        self.assertEqual(self.account1.funds, 900)
    
    def test_mobile_topup_invalid_number(self):
        """Test top-up with invalid mobile number"""
        test_cases = [
            ("12345678", "Invalid prefix"),
            ("1712345", "Too short"),
            ("771234567", "Too long"),
            ("77abc123", "Non-digits"),
            ("", "Empty string")
        ]
        
        for number, description in test_cases:
            with self.subTest(number=number, description=description):
                with self.assertRaises(InvalidInputError):
                    self.account1.mobile_topup(100, number)
    
    def test_mobile_topup_insufficient_funds(self):
        """Test mobile top-up with insufficient funds"""
        with self.assertRaises(InsufficientFundsError):
            self.account1.mobile_topup(1500, "77123456")
    
    def test_change_password_valid(self):
        """Test changing to a valid password"""
        self.assertTrue(self.account1.change_password("4321"))
        self.assertEqual(self.account1.passcode, "4321")
    
    def test_change_password_invalid(self):
        """Test changing to invalid passwords"""
        test_cases = [
            ("123", "Too short"),
            ("12345", "Too long"),
            ("abcd", "Non-digits"),
            ("", "Empty string")
        ]
        
        for password, description in test_cases:
            with self.subTest(password=password, description=description):
                with self.assertRaises(InvalidInputError):
                    self.account1.change_password(password)

class TestBankingGUI(unittest.TestCase):
    def setUp(self):
        """Set up GUI tests with a root window"""
        self.root = Tk()
        self.root.withdraw()  # Hide the window during tests
        self.app = BankingGUI(self.root)
    
    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()
    
    def test_account_creation(self):
        """Test that accounts are created correctly"""
    # First show the create account screen to initialize the widgets
        self.app.show_create_account()
    
    # Now test with mocked random values
        with patch('random.randint', side_effect=[54321, 9999]):
            # Get the account_type variable that was created in show_create_account()
            account_type_var = self.app.account_type
            
            # Set to Personal account type and create
            account_type_var.set("Personal")
            self.app.create_account()
            
            # Verify the account was created correctly
            self.assertIn("54321", self.app.accounts)
            self.assertEqual(self.app.accounts["54321"].passcode, "9999")
            self.assertEqual(self.app.accounts["54321"].account_category, "Personal")
    
    def test_successful_login(self):
        """Test successful login with correct credentials"""
        # Create a test account
        test_account = BankAccount("11111", "2222", "Personal")
        self.app.accounts["11111"] = test_account
        
        # Mock the entry widgets
        self.app.login_id = Mock()
        self.app.login_pass = Mock()
        self.app.login_id.get.return_value = "11111"
        self.app.login_pass.get.return_value = "2222"
        
        # Test login
        self.app.login()
        self.assertEqual(self.app.current_account, test_account)
    
    def test_failed_login(self):
        """Test login with invalid credentials"""
        # Create a test account
        test_account = BankAccount("11111", "2222", "Personal")
        self.app.accounts["11111"] = test_account
        
        # Test cases: (id, passcode, description)
        test_cases = [
            ("11111", "wrong", "Wrong password"),
            ("99999", "2222", "Wrong ID"),
            ("", "", "Empty fields"),
            ("abcde", "2222", "Non-numeric ID")
        ]
        
        for id, passcode, description in test_cases:
            with self.subTest(description=description):
                # Reset the current account
                self.app.current_account = None
                
                # Mock the entry widgets
                self.app.login_id = Mock()
                self.app.login_pass = Mock()
                self.app.login_id.get.return_value = id
                self.app.login_pass.get.return_value = passcode
                
                with patch('tkinter.messagebox.showerror') as mock_error:
                    self.app.login()
                    mock_error.assert_called_once()
                self.assertIsNone(self.app.current_account)
    
    def test_deposit_processing(self):
        """Test processing of deposit operations"""
        test_account = BankAccount("12345", "1234", "Personal", 1000)
        self.app.current_account = test_account
        
        # Mock the entry widget
        self.app.amount_entry = Mock()
        
        # Test valid deposit
        self.app.amount_entry.get.return_value = "500"
        with patch('tkinter.messagebox.showinfo'):
            self.app.do_deposit()
        self.assertEqual(test_account.funds, 1500)
        
        # Test invalid deposit (negative amount)
        self.app.amount_entry.get.return_value = "-100"
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_deposit()
            mock_error.assert_called_once()
        self.assertEqual(test_account.funds, 1500)  # Balance shouldn't change
        
        # Test invalid deposit (non-numeric)
        self.app.amount_entry.get.return_value = "abc"
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_deposit()
            mock_error.assert_called_once()
        self.assertEqual(test_account.funds, 1500)  # Balance shouldn't change
    
    def test_withdraw_processing(self):
        """Test processing of withdrawal operations"""
        test_account = BankAccount("12345", "1234", "Personal", 1000)
        self.app.current_account = test_account
        
        # Mock the entry widget
        self.app.amount_entry = Mock()
        
        # Test valid withdrawal
        self.app.amount_entry.get.return_value = "500"
        with patch('tkinter.messagebox.showinfo'):
            self.app.do_withdraw()
        self.assertEqual(test_account.funds, 500)
        
        # Test insufficient funds
        self.app.amount_entry.get.return_value = "1500"
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_withdraw()
            mock_error.assert_called_once()
        self.assertEqual(test_account.funds, 500)  # Balance shouldn't change
        
        # Test invalid withdrawal (negative amount)
        self.app.amount_entry.get.return_value = "-100"
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_withdraw()
            mock_error.assert_called_once()
        self.assertEqual(test_account.funds, 500)  # Balance shouldn't change
    
    def test_transfer_processing(self):
        """Test processing of transfer operations"""
        # Set up accounts
        sender = BankAccount("11111", "1234", "Personal", 1000)
        recipient = BankAccount("22222", "5678", "Business", 500)
        self.app.accounts = {"11111": sender, "22222": recipient}
        self.app.current_account = sender
        
        # Mock the entry widgets
        self.app.recipient_entry = Mock()
        self.app.amount_entry = Mock()
        
        # Test valid transfer
        self.app.recipient_entry.get.return_value = "22222"
        self.app.amount_entry.get.return_value = "300"
        
        with patch('tkinter.messagebox.showinfo'):
            self.app.do_transfer()
        
        self.assertEqual(sender.funds, 700)
        self.assertEqual(recipient.funds, 800)
        
        # Test invalid recipient
        self.app.recipient_entry.get.return_value = "99999"
        self.app.amount_entry.get.return_value = "100"
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_transfer()
            mock_error.assert_called_once()
        
        # Balances shouldn't change
        self.assertEqual(sender.funds, 700)
        self.assertEqual(recipient.funds, 800)
    
    def test_mobile_topup_processing(self):
        """Test processing of mobile top-up operations"""
        test_account = BankAccount("12345", "1234", "Personal", 1000)
        self.app.current_account = test_account
        
        # Mock the entry widgets
        self.app.mobile_entry = Mock()
        self.app.amount_entry = Mock()
        
        # Test valid top-up
        self.app.mobile_entry.get.return_value = "77123456"
        self.app.amount_entry.get.return_value = "100"
        
        with patch('tkinter.messagebox.showinfo'):
            self.app.do_mobile_topup()
        
        self.assertEqual(test_account.funds, 900)
        
        # Test invalid mobile number
        self.app.mobile_entry.get.return_value = "12345678"  # Invalid prefix
        self.app.amount_entry.get.return_value = "100"
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_mobile_topup()
            mock_error.assert_called_once()
        
        # Balance shouldn't change
        self.assertEqual(test_account.funds, 900)
    
    def test_password_change_processing(self):
        """Test processing of password change operations"""
        test_account = BankAccount("12345", "1234", "Personal", 1000)
        self.app.current_account = test_account
        
        # Mock the entry widgets
        self.app.new_pass_entry = Mock()
        self.app.confirm_pass_entry = Mock()
        
        # Test valid password change
        self.app.new_pass_entry.get.return_value = "4321"
        self.app.confirm_pass_entry.get.return_value = "4321"
        
        with patch('tkinter.messagebox.showinfo'):
            self.app.do_change_password()
        
        self.assertEqual(test_account.passcode, "4321")
        
        # Test non-matching passwords
        self.app.new_pass_entry.get.return_value = "4321"
        self.app.confirm_pass_entry.get.return_value = "1234"
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.do_change_password()
            mock_error.assert_called_once()
        
        # Password shouldn't change
        self.assertEqual(test_account.passcode, "4321")

if __name__ == '__main__':
    unittest.main(verbosity=2)