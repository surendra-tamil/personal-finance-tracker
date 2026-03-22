import json
from datetime import datetime
from pathlib import Path
from transaction import Transaction

class TransactionManager:
    """
    Manages all financial transactions.
    
    Handles adding, removing, filtering, and calculating statistics
    on transactions. Provides persistence through JSON file storage.
    """
    
    def __init__(self, data_file='data/transactions.json'):
        self.data_file = Path(data_file)
        self.transactions = []
        self.load_transactions()
    
    def add_transaction(self, amount, category, description):
        """
        Add a new transaction.
        
        Args:
            amount (float): Transaction amount
            category (str): Transaction category
            description (str): Transaction description
        
        Returns:
            Transaction: The created transaction object
        
        Raises:
            ValueError: If amount is negative or zero
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        transaction = Transaction(amount, category, description)
        self.transactions.append(transaction)
        self.save_transactions()
        return transaction
    
    def remove_transaction(self, transaction_id):
        """
        Remove a transaction by ID.
        
        Args:
            transaction_id (int): ID of transaction to remove
        
        Returns:
            bool: True if removed, False if not found
        """
        initial_length = len(self.transactions)
        self.transactions = [t for t in self.transactions if t.transaction_id != transaction_id]
        
        if len(self.transactions) < initial_length:
            self.save_transactions()
            return True
        return False
    
    def get_transactions_by_category(self, category):
        """
        Get all transactions in a specific category.
        
        Args:
            category (str): Category to filter by
        
        Returns:
            list: List of Transaction objects in that category
        """
        return [t for t in self.transactions if t.category.lower() == category.lower()]
    
    def get_transactions_by_date_range(self, start_date, end_date):
        """
        Get transactions within a date range.
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
        
        Returns:
            list: List of Transaction objects in date range
        """
        return [t for t in self.transactions if start_date <= t.date <= end_date]
    
    def calculate_total_spending(self):
        """
        Calculate total spending across all transactions.
        
        Returns:
            float: Total amount spent
        """
        return sum(t.amount for t in self.transactions)
    
    def calculate_category_spending(self):
        """
        Calculate spending by category.
        
        Returns:
            dict: Dictionary with categories as keys and total spending as values
        """
        category_totals = {}
        for transaction in self.transactions:
            if transaction.category not in category_totals:
                category_totals[transaction.category] = 0
            category_totals[transaction.category] += transaction.amount
        
        return category_totals
    
    def calculate_monthly_spending(self, month, year):
        """
        Calculate total spending for a specific month.
        
        Args:
            month (int): Month number (1-12)
            year (int): Year
        
        Returns:
            float: Total spending for the month
        """
        monthly_total = sum(
            t.amount for t in self.transactions
            if t.date.month == month and t.date.year == year
        )
        return monthly_total
    
    def save_transactions(self):
        """Save all transactions to JSON file."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = [t.to_dict() for t in self.transactions]
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_transactions(self):
        """Load transactions from JSON file."""
        if not self.data_file.exists():
            self.transactions = []
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.transactions = [Transaction.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError):
            print("Error loading transactions. Starting fresh.")
            self.transactions = []
    
    def get_all_transactions(self):
        """Get all transactions sorted by date (newest first)."""
        return sorted(self.transactions, key=lambda t: t.date, reverse=True)
