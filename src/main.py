from transaction_manager import TransactionManager
from datetime import datetime

def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("       PERSONAL FINANCE TRACKER")
    print("="*50)
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. View Transactions by Category")
    print("4. View Monthly Summary")
    print("5. View Category Summary")
    print("6. Remove Transaction")
    print("7. Exit")
    print("="*50)

def add_transaction(manager):
    """Add a new transaction."""
    try:
        amount = float(input("Enter amount: Rs "))
        category = input("Enter category (Food/Transport/Entertainment/Other): ")
        description = input("Enter description: ")
        
        manager.add_transaction(amount, category, description)
        print("✓ Transaction added successfully!")
    except ValueError as e:
        print(f"✗ Error: {e}")

def view_all_transactions(manager):
    """Display all transactions."""
    transactions = manager.get_all_transactions()
    
    if not transactions:
        print("\nNo transactions found.")
        return
    
    print("\n" + "="*70)
    print("ALL TRANSACTIONS")
    print("="*70)
    print(f"{'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<25}")
    print("-"*70)
    
    for t in transactions:
        print(f"{t.date.strftime('%Y-%m-%d'):<12} {t.category:<15} Rs{t.amount:<11.2f} {t.description:<25}")
    
    print("-"*70)
    print(f"Total Spending: Rs{manager.calculate_total_spending():.2f}")

def view_by_category(manager):
    """View transactions by category."""
    category = input("Enter category: ")
    transactions = manager.get_transactions_by_category(category)
    
    if not transactions:
        print(f"\nNo transactions found for category: {category}")
        return
    
    print(f"\n{'Date':<12} {'Amount':<12} {'Description':<30}")
    print("-"*55)
    
    for t in transactions:
        print(f"{t.date.strftime('%Y-%m-%d'):<12} Rs{t.amount:<11.2f} {t.description:<30}")
    
    total = sum(t.amount for t in transactions)
    print("-"*55)
    print(f"Total for {category}: Rs{total:.2f}")

def view_monthly_summary(manager):
    """View spending summary for a specific month."""
    try:
        month = int(input("Enter month (1-12): "))
        year = int(input("Enter year: "))
        
        if not (1 <= month <= 12):
            print("Invalid month!")
            return
        
        total = manager.calculate_monthly_spending(month, year)
        print(f"\nTotal spending for {month}/{year}: Rs{total:.2f}")
    except ValueError:
        print("Invalid input!")

def view_category_summary(manager):
    """View spending summary by category."""
    category_totals = manager.calculate_category_spending()
    
    if not category_totals:
        print("\nNo transactions found.")
        return
    
    print("\n" + "="*40)
    print("SPENDING BY CATEGORY")
    print("="*40)
    
    for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (total / manager.calculate_total_spending()) * 100
        print(f"{category:<20} Rs{total:>10.2f} ({percentage:>5.1f}%)")
    
    print("="*40)
    print(f"{'TOTAL':<20} Rs{manager.calculate_total_spending():>10.2f}")

def remove_transaction(manager):
    """Remove a transaction."""
    view_all_transactions(manager)
    
    try:
        transactions = manager.get_all_transactions()
        index = int(input("\nEnter transaction number to remove (starting from 1): ")) - 1
        
        if 0 <= index < len(transactions):
            transaction_id = transactions[index].transaction_id
            if manager.remove_transaction(transaction_id):
                print("✓ Transaction removed successfully!")
            else:
                print("✗ Failed to remove transaction.")
        else:
            print("Invalid transaction number!")
    except ValueError:
        print("Invalid input!")

def main():
    """Main application loop."""
    manager = TransactionManager()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            add_transaction(manager)
        elif choice == '2':
            view_all_transactions(manager)
        elif choice == '3':
            view_by_category(manager)
        elif choice == '4':
            view_monthly_summary(manager)
        elif choice == '5':
            view_category_summary(manager)
        elif choice == '6':
            remove_transaction(manager)
        elif choice == '7':
            print("\nThank you for using Personal Finance Tracker!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
