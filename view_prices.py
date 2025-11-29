#!/usr/bin/env python3
"""
View collected prices from the database.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import PriceDatabase


def view_all_prices():
    """Display all recent prices for all products."""
    db = PriceDatabase()

    products = db.get_all_products()

    if not products:
        print("No products found in database")
        db.close()
        return

    print("=" * 70)
    print("PRICE HISTORY")
    print("=" * 70)

    for product in products:
        print(f"\n{product.name} ({product.size})")
        print(f"UPC: {product.upc}")
        print("-" * 70)

        retailers = ['walmart', 'target', 'cvs', 'walgreens', 'amazon']

        for retailer_id in retailers:
            recent_prices = db.get_recent_prices(product.id, retailer_id, limit=5)

            if recent_prices:
                print(f"\n{retailer_id.capitalize()}:")
                for price_point in recent_prices:
                    timestamp = price_point.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    print(f"  {timestamp} - ${price_point.price:.2f}")
            else:
                print(f"\n{retailer_id.capitalize()}: No prices recorded")

        print()

    db.close()


if __name__ == "__main__":
    view_all_prices()
