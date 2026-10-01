import sqlite3
import json
import logging
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

class DatabaseLoader:
    def __init__(self, db_name: str = "production_etl.db"):
        self.db_name = db_name
        logger.info(f"Day 9: Database Loader Engine connected to '{self.db_name}'.")

    def initialize_database(self):
        """Day 8 Setup: Enforcing structural table schemas."""
        query = """
        CREATE TABLE IF NOT EXISTS clean_users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            username TEXT,
            email TEXT,
            geo_lat REAL,
            geo_lng REAL,
            full_address TEXT,
            company_name TEXT,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Database Initialization failed: {str(e)}")
            raise e

    def load_records(self, processed_records: List[Dict[str, Any]]):
        """
        Day 9 Core Task: Transformed rows ko relational database me 
        safe batch insertions ke through load karta hai.
        """
        insert_query = """
        INSERT OR REPLACE INTO clean_users 
        (id, name, username, email, geo_lat, geo_lng, full_address, company_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                
                inserted_count = 0
                for row in processed_records:
                    # JSON values ko SQL parameterized tuple me convert karna for security
                    record_data = (
                        row.get("id"),
                        row.get("name"),
                        row.get("username"),
                        row.get("email"),
                        row.get("geo_lat"),
                        row.get("geo_lng"),
                        row.get("full_address"),
                        row.get("company_name")
                    )
                    cursor.execute(insert_query, record_data)
                    inserted_count += 1
                
                connection.commit()
                logger.info(f"💾 Success: Successfully loaded {inserted_count} production rows into 'clean_users' table.")
                
        except sqlite3.Error as e:
            logger.error(f"❌ Database Insertion Loop Failed: {str(e)}")

# --- Production Simulation Test ---
if __name__ == "__main__":
    print("🚀 Day 9 Pipeline: Executing Live Data Loading Process...\n")
    
    loader = DatabaseLoader()
    loader.initialize_database()
    
    # Day 7 ke data target mapping se static simulation stream array read kar rahe hain
    try:
        with open("clean_transformed_data.json", "read", encoding="utf-8") as f:
            mock_pipeline_data = json.load(f)
    except:
        # Fallback agar file read access block ho local env me
        mock_pipeline_data = [{
            "id": 10,
            "name": "Kunal Sharma",
            "username": "kunals",
            "email": "kunal@tier1.com",
            "geo_lat": 28.6139,
            "geo_lng": 77.2090,
            "full_address": "Connaught Place, New Delhi",
            "company_name": "Tier-1 Tech Corp"
        }]

    # Running insertion automation
    loader.load_records(mock_pipeline_data)
    print("\n✅ Day 9 Task Complete: Transformed records are now persistently loaded into the SQL engine.")
