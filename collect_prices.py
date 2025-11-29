#!/usr/bin/env python3
"""
Automated price collection script.
Reads products from database and collects prices from all configured retailers.
"""
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import PriceDatabase
from src.scraper import WalmartScraper, TargetScraper, CVSScraper, WalgreensScraper, AmazonScraper


def collect_prices_for_all_products():
    """Collect prices for all products in the database."""
    print("=" * 70)
    print("AUTOMATED PRICE COLLECTION")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    db = PriceDatabase()

    # Initialize scrapers
    scrapers = {
        'walmart': WalmartScraper(),
        'target': TargetScraper(),
        'cvs': CVSScraper(),
        'walgreens': WalgreensScraper(),
        'amazon': AmazonScraper()
    }

    # Get all products
    products = db.get_all_products()

    if not products:
        print("\n⚠️  No products found in database")
        print("Run migrate_add_product_urls.py to add products")
        db.close()
        return

    print(f"\nFound {len(products)} product(s) to track\n")

    total_attempts = 0
    total_successes = 0
    total_failures = 0

    # Process each product
    for product in products:
        print("=" * 70)
        print(f"Product: {product.name} ({product.size})")
        print(f"ID: {product.id}")
        print(f"UPC: {product.upc}")
        print("=" * 70)

        product_successes = 0
        product_failures = 0

        # Try each retailer
        for retailer_id, scraper in scrapers.items():
            url = product.get_retailer_url(retailer_id)

            if not url:
                print(f"\n⊘ {retailer_id.capitalize():<12} - No URL configured (skipping)")
                continue

            print(f"\n→ {retailer_id.capitalize():<12} - Scraping...")
            total_attempts += 1

            try:
                price_point = scraper.fetch_price(product.id, url)

                if price_point:
                    # Save to database
                    db.add_price_point(price_point)
                    print(f"  ✓ SUCCESS: ${price_point.price:.2f} (saved to database)")
                    product_successes += 1
                    total_successes += 1
                else:
                    print(f"  ✗ FAILED: No price returned")
                    product_failures += 1
                    total_failures += 1

            except Exception as e:
                print(f"  ✗ ERROR: {e}")
                product_failures += 1
                total_failures += 1

        # Product summary
        print(f"\n{'-' * 70}")
        print(f"Product Summary: {product_successes} successful, {product_failures} failed")
        print(f"{'-' * 70}\n")

    # Overall summary
    print("\n" + "=" * 70)
    print("COLLECTION COMPLETE")
    print("=" * 70)
    print(f"Total attempts: {total_attempts}")
    print(f"Successful: {total_successes} ({total_successes/total_attempts*100:.1f}%)" if total_attempts > 0 else "Successful: 0")
    print(f"Failed: {total_failures} ({total_failures/total_attempts*100:.1f}%)" if total_attempts > 0 else "Failed: 0")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    db.close()


def collect_prices_for_product(product_id: str):
    """Collect prices for a specific product."""
    print("=" * 70)
    print(f"COLLECTING PRICES FOR: {product_id}")
    print("=" * 70)

    db = PriceDatabase()

    # Get the product
    product = db.get_product(product_id)

    if not product:
        print(f"\n✗ Product not found: {product_id}")
        db.close()
        return

    print(f"\nProduct: {product.name} ({product.size})")
    print(f"UPC: {product.upc}\n")

    # Initialize scrapers
    scrapers = {
        'walmart': WalmartScraper(),
        'target': TargetScraper(),
        'cvs': CVSScraper(),
        'walgreens': WalgreensScraper(),
        'amazon': AmazonScraper()
    }

    successes = 0
    failures = 0

    # Try each retailer
    for retailer_id, scraper in scrapers.items():
        url = product.get_retailer_url(retailer_id)

        if not url:
            print(f"{retailer_id.capitalize():<12} - No URL configured (skipping)")
            continue

        print(f"{retailer_id.capitalize():<12} - ", end='', flush=True)

        try:
            price_point = scraper.fetch_price(product.id, url)

            if price_point:
                db.add_price_point(price_point)
                print(f"✓ ${price_point.price:.2f}")
                successes += 1
            else:
                print(f"✗ Failed")
                failures += 1

        except Exception as e:
            print(f"✗ Error: {e}")
            failures += 1

    print(f"\n{'-' * 70}")
    print(f"Results: {successes} successful, {failures} failed")
    print(f"{'-' * 70}")

    db.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Collect for specific product
        product_id = sys.argv[1]
        collect_prices_for_product(product_id)
    else:
        # Collect for all products
        collect_prices_for_all_products()
