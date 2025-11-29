"""
Script to find price selectors for different retailers.
Saves HTML and prints potential price elements.
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time
import re


def find_price_selector(url, retailer_name):
    """Find price selector for a retailer"""
    print(f"\n{'='*60}")
    print(f"Finding price selector for {retailer_name}")
    print(f"{'='*60}")

    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--width=1920')
    firefox_options.add_argument('--height=1080')

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript

        # Common price selectors to try
        selectors = [
            '[data-test*="price"]',
            '[class*="price"]',
            '[itemprop="price"]',
            '[data-automation-id*="price"]',
            'span[class*="Price"]',
            'div[class*="Price"]',
            '.price',
        ]

        found_prices = []

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    text = elem.text.strip()
                    if text and re.search(r'\$\d+', text):
                        found_prices.append({
                            'selector': selector,
                            'text': text,
                            'tag': elem.tag_name,
                            'classes': elem.get_attribute('class')
                        })
            except:
                continue

        if found_prices:
            print(f"\n✓ Found {len(found_prices)} price elements:")
            for i, price in enumerate(found_prices[:5], 1):
                print(f"\n  {i}. Text: {price['text']}")
                print(f"     Selector: {price['selector']}")
                print(f"     Tag: {price['tag']}")
                print(f"     Classes: {price['classes']}")
        else:
            print("\n✗ No price elements found")
            print("Saving page source for manual inspection...")
            with open(f'/Users/macbookpro2025/Sites/price-intelligence-tracker/debug_{retailer_name}.html', 'w') as f:
                f.write(driver.page_source)
            print(f"Saved to debug_{retailer_name}.html")

        return found_prices

    finally:
        driver.quit()


# Test URLs for each retailer
retailers = {
    'walmart': 'https://www.walmart.com/ip/Eucerin-Advanced-Repair-Body-Lotion-Fragrance-Free-16-9-fl-oz-Bottle/10811050',
    'cvs': 'https://www.cvs.com/shop/eucerin-advanced-repair-lotion-16-9-oz-prodid-1011766',
    'walgreens': 'https://www.walgreens.com/store/c/eucerin-advanced-repair-body-lotion/ID=prod3970669-product',
    'amazon': 'https://www.amazon.com/Eucerin-Advanced-Repair-Lotion-Ounce/dp/B003BMJGKE',
}

if __name__ == "__main__":
    results = {}
    for name, url in retailers.items():
        try:
            results[name] = find_price_selector(url, name)
            time.sleep(2)  # Be nice to servers
        except Exception as e:
            print(f"\n✗ Error testing {name}: {e}")
            results[name] = None

    print(f"\n\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, prices in results.items():
        if prices:
            print(f"\n{name.upper()}: Found {len(prices)} price elements")
            if prices:
                print(f"  Best selector: {prices[0]['selector']}")
                print(f"  Price: {prices[0]['text']}")
        else:
            print(f"\n{name.upper()}: No prices found (check debug_{name}.html)")
