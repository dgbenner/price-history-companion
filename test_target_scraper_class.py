"""Test the updated TargetScraper class"""
import sys
sys.path.insert(0, '/Users/macbookpro2025/Sites/price-intelligence-tracker')

from src.scraper import TargetScraper

def test_target_scraper():
    """Test TargetScraper with a real product"""
    scraper = TargetScraper()

    product_id = "eucerin-advanced-repair-16.9oz"
    url = "https://www.target.com/p/eucerin-advanced-repair-unscented-body-lotion-for-dry-skin-16-9-fl-oz/-/A-11005178"

    print("=" * 60)
    print("Testing TargetScraper class")
    print("=" * 60)
    print(f"Product ID: {product_id}")
    print(f"URL: {url}\n")

    price_point = scraper.fetch_price(product_id, url)

    if price_point:
        print("\n✓ SUCCESS!")
        print(f"  Product ID: {price_point.product_id}")
        print(f"  Retailer: {price_point.retailer_id}")
        print(f"  Price: ${price_point.price:.2f}")
        print(f"  Timestamp: {price_point.timestamp}")
        print(f"  URL: {price_point.url}")
    else:
        print("\n✗ FAILED - Could not fetch price")

if __name__ == "__main__":
    test_target_scraper()
