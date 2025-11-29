"""
Test script to fetch price from Target using Selenium.

This demonstrates how to use Selenium to scrape prices from JavaScript-heavy sites.
"""
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time


def fetch_target_price(url: str):
    """
    Fetch price from a Target product page using Selenium.

    Args:
        url: Target product URL

    Returns:
        Price as float, or None if not found
    """
    # Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in background (no browser window)
    firefox_options.add_argument('--width=1920')
    firefox_options.add_argument('--height=1080')
    firefox_options.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # Initialize the driver
    print("Starting Firefox browser...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Navigate to the URL
        print(f"Loading page: {url}")
        driver.get(url)

        # Wait for the page to load (give JavaScript time to render)
        print("Waiting for page to load...")
        time.sleep(3)  # Simple wait - can be replaced with explicit waits

        # Try multiple selectors to find the price
        price_selectors = [
            # Common Target price selectors
            (By.CSS_SELECTOR, '[data-test="product-price"]'),
            (By.CSS_SELECTOR, '.h-text-bs'),
            (By.CSS_SELECTOR, '[itemprop="price"]'),
            (By.XPATH, '//*[contains(@class, "Price")]//span'),
            (By.XPATH, '//*[contains(text(), "$")]'),
        ]

        price_text = None

        for by, selector in price_selectors:
            try:
                print(f"Trying selector: {selector}")
                # Wait up to 10 seconds for element to appear
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((by, selector))
                )
                price_text = element.text
                print(f"  Found text: {price_text}")

                # Check if it looks like a price
                if '$' in price_text:
                    print(f"✓ Found price element: {price_text}")
                    break
            except Exception as e:
                print(f"  Selector failed: {str(e)[:50]}")
                continue

        if not price_text:
            print("\n⚠ Could not find price with any selector")
            print("Saving page source for debugging...")
            with open('/Users/macbookpro2025/Sites/price-intelligence-tracker/debug_target_page.html', 'w') as f:
                f.write(driver.page_source)
            print("Page source saved to debug_target_page.html")
            return None

        # Extract numeric price from text like "$12.99" or "12.99"
        import re
        price_match = re.search(r'\$?(\d+\.\d{2})', price_text)
        if price_match:
            price = float(price_match.group(1))
            print(f"\n✓ SUCCESS! Extracted price: ${price:.2f}")
            return price
        else:
            print(f"\n⚠ Could not parse price from: {price_text}")
            return None

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None

    finally:
        # Always close the browser
        print("\nClosing browser...")
        driver.quit()


if __name__ == "__main__":
    # Test URL
    url = "https://www.target.com/p/eucerin-advanced-repair-unscented-body-lotion-for-dry-skin-16-9-fl-oz/-/A-11005178"

    print("=" * 60)
    print("Testing Target Price Scraper with Selenium")
    print("=" * 60)

    price = fetch_target_price(url)

    if price:
        print(f"\n{'='*60}")
        print(f"FINAL RESULT: ${price:.2f}")
        print(f"{'='*60}")
    else:
        print("\n⚠ Failed to fetch price. Check debug output above.")
