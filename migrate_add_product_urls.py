#!/usr/bin/env python3
"""
Migration script to add retailer URL columns to products table and insert Eucerin product.
"""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.models import Product
from src.database import PriceDatabase


def migrate_database():
    """Migrate the database to add new product fields."""
    db_path = "data/prices.db"

    print(f"Migrating database: {db_path}")

    # Connect directly to check if migration is needed
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check current schema
    cursor.execute("PRAGMA table_info(products)")
    columns = {row[1] for row in cursor.fetchall()}

    print(f"Current columns: {columns}")

    # Check if migration needed
    new_columns = {'upc', 'target_url', 'walmart_url', 'cvs_url', 'walgreens_url', 'amazon_url', 'created_at', 'updated_at'}
    missing_columns = new_columns - columns

    if missing_columns:
        print(f"Adding missing columns: {missing_columns}")

        # Add columns one by one (SQLite doesn't support adding multiple columns at once)
        now = datetime.now().isoformat()

        if 'upc' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN upc TEXT")
        if 'target_url' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN target_url TEXT")
        if 'walmart_url' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN walmart_url TEXT")
        if 'cvs_url' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN cvs_url TEXT")
        if 'walgreens_url' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN walgreens_url TEXT")
        if 'amazon_url' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN amazon_url TEXT")
        if 'created_at' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN created_at TEXT")
            # Set created_at for existing products
            cursor.execute("UPDATE products SET created_at = ? WHERE created_at IS NULL", (now,))
        if 'updated_at' in missing_columns:
            cursor.execute("ALTER TABLE products ADD COLUMN updated_at TEXT")
            # Set updated_at for existing products
            cursor.execute("UPDATE products SET updated_at = ? WHERE updated_at IS NULL", (now,))

        conn.commit()
        print("✓ Migration completed")
    else:
        print("✓ Database already has all required columns")

    conn.close()


def add_eucerin_product():
    """Add the Eucerin Advanced Repair Lotion product with all retailer URLs."""
    print("\nAdding Eucerin product...")

    db = PriceDatabase()

    eucerin = Product(
        id="eucerin-advanced-repair-lotion-16.9oz",
        name="Eucerin Advanced Repair Lotion",
        size="16.9 oz",
        category="skincare",
        upc="072140634827",
        target_url="https://www.target.com/p/eucerin-advanced-repair-unscented-body-lotion-for-dry-skin-16-9-fl-oz/-/A-11005178",
        walmart_url="https://www.walmart.com/ip/Eucerin-Advanced-Repair-Body-Lotion-Fragrance-Free-16-9-fl-oz-Bottle/10811050",
        cvs_url="https://www.cvs.com/shop/eucerin-advanced-repair-body-lotion-16-9-oz-prodid-1016602",
        walgreens_url="https://www.walgreens.com/store/c/eucerin-advanced-repair-body-lotion/ID=prod3970669-product",
        amazon_url="https://www.amazon.com/Eucerin-Advanced-Repair-Lotion-Ounce/dp/B003BMJGKE"
    )

    db.add_product(eucerin)
    print(f"✓ Added product: {eucerin.name} ({eucerin.size})")
    print(f"  Product ID: {eucerin.id}")
    print(f"  UPC: {eucerin.upc}")
    print(f"  Target: {eucerin.target_url[:50]}...")
    print(f"  Walmart: {eucerin.walmart_url[:50]}...")
    print(f"  CVS: {eucerin.cvs_url[:50]}...")
    print(f"  Walgreens: {eucerin.walgreens_url[:50]}...")
    print(f"  Amazon: {eucerin.amazon_url[:50]}...")

    # Verify it was added
    retrieved = db.get_product(eucerin.id)
    if retrieved:
        print(f"\n✓ Verification: Product successfully stored in database")
        print(f"  Retrieved: {retrieved.name}")
        print(f"  Has Target URL: {bool(retrieved.target_url)}")
        print(f"  Has Walmart URL: {bool(retrieved.walmart_url)}")
        print(f"  Has CVS URL: {bool(retrieved.cvs_url)}")
        print(f"  Has Walgreens URL: {bool(retrieved.walgreens_url)}")
        print(f"  Has Amazon URL: {bool(retrieved.amazon_url)}")
    else:
        print("\n✗ Error: Could not retrieve product from database")

    db.close()


if __name__ == "__main__":
    print("=" * 70)
    print("DATABASE MIGRATION: Add Product URLs")
    print("=" * 70)

    migrate_database()
    add_eucerin_product()

    print("\n" + "=" * 70)
    print("Migration complete!")
    print("=" * 70)
