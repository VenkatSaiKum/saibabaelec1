"""
Clean Database Script
Removes all products, bills, and bills history
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'electrical_shop.db')

def clean_database():
    """Remove all products, bills (transactions), and related data"""
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        print("Starting database cleanup...")
        
        # Delete transaction items first (foreign key constraint)
        cursor.execute('DELETE FROM transaction_items')
        transaction_items_count = cursor.rowcount
        print(f"✓ Deleted {transaction_items_count} transaction items")
        
        # Delete all transactions (bills)
        cursor.execute('DELETE FROM transactions')
        transactions_count = cursor.rowcount
        print(f"✓ Deleted {transactions_count} bills")
        
        # Delete all supplier bill items
        cursor.execute('DELETE FROM supplier_bill_items')
        supplier_items_count = cursor.rowcount
        print(f"✓ Deleted {supplier_items_count} supplier bill items")
        
        # Delete all supplier bills
        cursor.execute('DELETE FROM supplier_bills')
        supplier_bills_count = cursor.rowcount
        print(f"✓ Deleted {supplier_bills_count} supplier bills")
        
        # Delete all stock movements
        cursor.execute('DELETE FROM stock_movements')
        stock_movements_count = cursor.rowcount
        print(f"✓ Deleted {stock_movements_count} stock movements")
        
        # Delete all products
        cursor.execute('DELETE FROM products')
        products_count = cursor.rowcount
        print(f"✓ Deleted {products_count} products")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='products'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transaction_items'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='supplier_bills'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='supplier_bill_items'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='stock_movements'")
        
        connection.commit()
        print("\n✓ Database cleaned successfully!")
        print(f"Total records deleted: {transaction_items_count + transactions_count + supplier_items_count + supplier_bills_count + stock_movements_count + products_count}")
        
    except Exception as e:
        connection.rollback()
        print(f"Error during cleanup: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    response = input("Are you sure you want to delete all products, bills, and history? (yes/no): ")
    if response.lower() == 'yes':
        clean_database()
    else:
        print("Cleanup cancelled.")
