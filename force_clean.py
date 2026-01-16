"""
Force Clean Database - No confirmation required
Removes all products, bills, and bills history immediately
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'electrical_shop.db')

def force_clean_database():
    """Remove all products, bills (transactions), and related data"""
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = connection.cursor()
    
    try:
        print("Starting database cleanup...")
        total_deleted = 0
        
        # List of tables to clean (order matters for foreign keys)
        tables_to_clean = [
            ('transaction_items', 'transaction items'),
            ('transactions', 'bills'),
            ('supplier_bill_items', 'supplier bill items'),
            ('supplier_bills', 'supplier bills'),
            ('stock_movements', 'stock movements'),
            ('products', 'products'),
            ('expenses', 'expenses')
        ]
        
        for table_name, display_name in tables_to_clean:
            try:
                cursor.execute(f'DELETE FROM {table_name}')
                count = cursor.rowcount
                if count > 0:
                    print(f"✓ Deleted {count} {display_name}")
                    total_deleted += count
            except sqlite3.OperationalError:
                # Table doesn't exist, skip it
                pass
        
        # Reset auto-increment counters for all tables
        sequence_tables = ['products', 'transactions', 'transaction_items', 
                          'supplier_bills', 'supplier_bill_items', 'stock_movements', 'expenses']
        
        for table in sequence_tables:
            try:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
            except sqlite3.OperationalError:
                pass
        
        connection.commit()
        print("\n✓ Database cleaned successfully!")
        print(f"Total records deleted: {total_deleted}")
        
    except Exception as e:
        connection.rollback()
        print(f"✗ Error during cleanup: {e}")
        raise
    finally:
        connection.close()

if __name__ == '__main__':
    force_clean_database()
