"""Test all retailer scrapers"""
import sys
sys.path.insert(0, '/Users/macbookpro2025/Sites/price-intelligence-tracker')

from src.scraper import WalmartScraper, TargetScraper, WalgreensScraper, AmazonScraper, CVSScraper


def test_all_scrapers():
    """Test all scrapers with real product URLs"""

    test_products = [
        {
            'scraper': WalmartScraper(),
            'product_id': 'eucerin-advanced-repair-16.9oz-walmart',
            'url': 'https://www.walmart.com/ip/Eucerin-Advanced-Repair-Body-Lotion-Fragrance-Free-16-9-fl-oz-Bottle/10811050',
            'name': 'Walmart'
        },
        {
            'scraper': TargetScraper(),
            'product_id': 'eucerin-advanced-repair-16.9oz-target',
            'url': 'https://www.target.com/p/eucerin-advanced-repair-unscented-body-lotion-for-dry-skin-16-9-fl-oz/-/A-11005178',
            'name': 'Target'
        },
        {
            'scraper': WalgreensScraper(),
            'product_id': 'eucerin-advanced-repair-16.9oz-walgreens',
            'url': 'https://www.walgreens.com/store/c/eucerin-advanced-repair-body-lotion/ID=prod3970669-product',
            'name': 'Walgreens'
        },
        {
            'scraper': AmazonScraper(),
            'product_id': 'eucerin-advanced-repair-16oz-amazon',
            'url': 'https://www.amazon.com/Eucerin-Advanced-Repair-Lotion-Ounce/dp/B003BMJGKE',
            'name': 'Amazon'
        },
        {
            'scraper': CVSScraper(),
            'product_id': 'eucerin-advanced-repair-16.9oz-cvs',
            'url': 'https://www.cvs.com/shop/eucerin-advanced-repair-body-lotion-16-9-oz-prodid-1016602',
            'name': 'CVS'
        }
    ]

    print("=" * 70)
    print("TESTING ALL RETAILER SCRAPERS")
    print("=" * 70)

    results = []

    for product in test_products:
        print(f"\n{'='*70}")
        print(f"Testing {product['name']}")
        print(f"{'='*70}")

        try:
            price_point = product['scraper'].fetch_price(
                product['product_id'],
                product['url']
            )

            if price_point:
                print(f"✓ SUCCESS - Price: ${price_point.price:.2f}")
                results.append({
                    'retailer': product['name'],
                    'success': True,
                    'price': price_point.price
                })
            else:
                print(f"✗ FAILED - No price returned")
                results.append({
                    'retailer': product['name'],
                    'success': False,
                    'price': None
                })
        except Exception as e:
            print(f"✗ ERROR - {e}")
            results.append({
                'retailer': product['name'],
                'success': False,
                'price': None
            })

    # Summary
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    for result in results:
        status = "✓" if result['success'] else "✗"
        price_str = f"${result['price']:.2f}" if result['price'] else "N/A"
        print(f"{status} {result['retailer']:<15} - Price: {price_str}")

    success_count = sum(1 for r in results if r['success'])
    print(f"\nSuccessful: {success_count}/{len(results)}")


if __name__ == "__main__":
    test_all_scrapers()
