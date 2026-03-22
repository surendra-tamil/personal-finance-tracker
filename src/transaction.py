from datetime import datetime

class Transaction:
    """
    Represents a single financial transaction.
    
    Attributes:
        amount (float): The transaction amount
        category (str): Category of the transaction (e.g., 'Food', 'Transport')
        description (str): Description of the transaction
        date (datetime): Date of the transaction
        transaction_id (str): Unique identifier for the transaction
    """
    
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now()
        self.transaction_id = self._generate_id()
    
    def _generate_id(self):
        """Generate a unique transaction ID based on timestamp."""
        return int(self.date.timestamp() * 1000)
    
    def __str__(self):
        """String representation of the transaction."""
        return f"{self.date.strftime('%Y-%m-%d')} | {self.category:12} | Rs{self.amount:8.2f} | {self.description}"
    
    def to_dict(self):
        """Convert transaction to dictionary for JSON storage."""
        return {
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary."""
        return cls(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            date=datetime.fromisoformat(data['date'])
        )
