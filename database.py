import sqlite3
from typing import List, Optional
from models import Customer

class Database:
    def __init__(self, db_path: str = "customers.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT,
                phone TEXT,
                email TEXT,
                notes TEXT,
                remind_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def add_customer(self, customer: Customer) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customers (name, company, phone, email, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (customer.name, customer.company, customer.phone, customer.email, customer.notes))
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Customer(
                id=row[0],
                name=row[1],
                company=row[2],
                phone=row[3],
                email=row[4],
                notes=row[5],
                remind_date=row[6]
            )
        return None
    
    def update_customer(self, customer: Customer):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE customers 
            SET name = ?, company = ?, phone = ?, email = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (customer.name, customer.company, customer.phone, customer.email, customer.notes, customer.id))
        conn.commit()
        conn.close()
    
    def get_all_customers(self) -> List[Customer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        
        return [Customer(
            id=row[0],
            name=row[1],
            company=row[2],
            phone=row[3],
            email=row[4],
            notes=row[5],
            remind_date=row[6]
        ) for row in rows]
    
    def search_customers(self, query: str) -> List[Customer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM customers 
            WHERE name LIKE ? OR company LIKE ?
            ORDER BY name
        """, (f"%{query}%", f"%{query}%"))
        rows = cursor.fetchall()
        conn.close()
        
        return [Customer(
            id=row[0],
            name=row[1],
            company=row[2],
            phone=row[3],
            email=row[4],
            notes=row[5],
            remind_date=row[6]
        ) for row in rows]
    
    def set_remind_date(self, customer_id: int, date: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE customers 
            SET remind_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (date, customer_id))
        conn.commit()
        conn.close()
    
    def get_customers_with_reminders(self) -> List[Customer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM customers 
            WHERE remind_date IS NOT NULL
            ORDER BY remind_date
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [Customer(
            id=row[0],
            name=row[1],
            company=row[2],
            phone=row[3],
            email=row[4],
            notes=row[5],
            remind_date=row[6]
        ) for row in rows]
