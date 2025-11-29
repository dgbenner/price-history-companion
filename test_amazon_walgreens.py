"""Retest Amazon and Walgreens scrapers"""
import sys
sys.path.insert(0, '/Users/macbookpro2025/Sites/price-intelligence-tracker')

from src.scraper import AmazonScraper, WalgreensScraper


def test_scrapers():
    """Test Amazon and Walgreens scrapers"""

    tests = [
        {
            'scraper': AmazonScraper(),
            'product_id': 'eucerin-advanced-repair-16oz-amazon',
            'url': 'https://www.amazon.com/Eucerin-Advanced-Repair-Lotion-Ounce/dp/B003BMJGKE',
            'name': 'Amazon'
        },
        {
            'scraper': WalgreensScraper(),
            'product_id': 'eucerin-advanced-repair-16.9oz-walgreens',
            'url': 'https://www.walgreens.com/store/c/eucerin-advanced-repair-body-lotion/ID=prod3970669-product',
            'name': 'Walgreens'
        },
    ]

    print("=" * 70)
    print("RETESTING AMAZON AND WALGREENS SCRAPERS")
    print("=" * 70)

    results = []

    for test in tests:
        print(f"\n{'='*70}")
        print(f"Testing {test['name']}")
        print(f"URL: {test['url']}")
        print(f"{'='*70}")

        try:
            price_point = test['scraper'].fetch_price(
                test['product_id'],
                test['url']
            )

            if price_point:
                print(f"\n✓ SUCCESS!")
                print(f"  Price: ${price_point.price:.2f}")
                print(f"  Product ID: {price_point.product_id}")
                print(f"  Retailer: {price_point.retailer_id}")
                print(f"  Timestamp: {price_point.timestamp}")
                results.append({
                    'retailer': test['name'],
                    'success': True,
                    'price': price_point.price
                })
            else:
                print(f"\n✗ FAILED - No price returned")
                results.append({
                    'retailer': test['name'],
                    'success': False,
                    'price': None
                })
        except Exception as e:
            print(f"\n✗ ERROR - {e}")
            import traceback
            traceback.print_exc()
            results.append({
                'retailer': test['name'],
                'success': False,
                'price': None
            })

    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    for result in results:
        status = "✓" if result['success'] else "✗"
        price_str = f"${result['price']:.2f}" if result['price'] else "FAILED"
        print(f"{status} {result['retailer']:<15} - {price_str}")

    success_count = sum(1 for r in results if r['success'])
    print(f"\nSuccessful: {success_count}/{len(results)}")


if __name__ == "__main__":
    test_scrapers()
