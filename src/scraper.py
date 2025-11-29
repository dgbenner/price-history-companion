"""
Price scraper framework.

This module provides the structure for fetching prices from retailers.
The actual scraping logic needs to be implemented based on each retailer's website.

NOTE: Web scraping may violate terms of service. Consider using:
1. Official APIs where available
2. RSS feeds or price tracking services
3. Manual data entry for prototype
"""
from datetime import datetime
from typing import Optional
import time
import json
import re

from src.models import PricePoint


class BaseScraper:
    """Base class for retailer scrapers."""
    
    def __init__(self, retailer_id: str):
        self.retailer_id = retailer_id
    
    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """
        Fetch current price for a product.
        
        Args:
            product_id: Product identifier
            url: Product URL at the retailer
        
        Returns:
            PricePoint if successful, None otherwise
        """
        raise NotImplementedError("Subclasses must implement fetch_price")
    
    def _extract_price(self, html: str) -> Optional[float]:
        """Extract price from HTML. Implement in subclass."""
        raise NotImplementedError
    
    def _extract_pack_size(self, html: str) -> int:
        """Extract pack size from HTML. Implement in subclass."""
        return 1  # Default to single item


class WalmartScraper(BaseScraper):
    """Scraper for Walmart.com using Selenium."""

    def __init__(self):
        super().__init__("walmart")

    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """Fetch current price from Walmart using Selenium."""
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.firefox import GeckoDriverManager

            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--width=1920')
            firefox_options.add_argument('--height=1080')

            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

            try:
                driver.get(url)
                time.sleep(3)

                # Walmart uses itemprop="price"
                price_selectors = [
                    (By.CSS_SELECTOR, '[itemprop="price"]'),
                    (By.CSS_SELECTOR, '[data-automation-id*="price"]'),
                ]

                price_text = None
                for by, selector in price_selectors:
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((by, selector))
                        )
                        price_text = element.text
                        if '$' in price_text:
                            break
                    except:
                        continue

                if not price_text:
                    print(f"Could not find price for {product_id}")
                    return None

                price_match = re.search(r'\$?(\d+\.\d{2})', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    return PricePoint(
                        product_id=product_id,
                        retailer_id=self.retailer_id,
                        price=price,
                        timestamp=datetime.now(),
                        url=url
                    )
                else:
                    print(f"Could not parse price from: {price_text}")
                    return None

            finally:
                driver.quit()

        except Exception as e:
            print(f"Error fetching Walmart price for {product_id}: {e}")
            return None

    def _extract_price(self, html: str) -> Optional[float]:
        """Not used - Selenium handles extraction."""
        _ = html
        return None


class TargetScraper(BaseScraper):
    """
    Scraper for Target.com using Selenium for JavaScript rendering.

    Uses Firefox with GeckoDriver to handle dynamic content.
    """

    def __init__(self):
        super().__init__("target")

    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """
        Fetch current price from Target using Selenium.

        Args:
            product_id: Product identifier
            url: Target product URL

        Returns:
            PricePoint if successful, None otherwise
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.firefox import GeckoDriverManager

            # Set up Firefox options for headless browsing
            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--width=1920')
            firefox_options.add_argument('--height=1080')
            firefox_options.set_preference(
                'general.useragent.override',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )

            # Initialize Firefox driver
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

            try:
                # Navigate to the URL
                driver.get(url)

                # Wait for page to load
                time.sleep(3)

                # Try to find the price element
                price_text = None
                price_selectors = [
                    (By.CSS_SELECTOR, '[data-test="product-price"]'),
                    (By.CSS_SELECTOR, '.h-text-bs'),
                    (By.CSS_SELECTOR, '[itemprop="price"]'),
                ]

                for by, selector in price_selectors:
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((by, selector))
                        )
                        price_text = element.text
                        if '$' in price_text:
                            break
                    except:
                        continue

                if not price_text:
                    print(f"Could not find price for {product_id}")
                    return None

                # Extract numeric price
                price_match = re.search(r'\$?(\d+\.\d{2})', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    return PricePoint(
                        product_id=product_id,
                        retailer_id=self.retailer_id,
                        price=price,
                        timestamp=datetime.now(),
                        url=url
                    )
                else:
                    print(f"Could not parse price from: {price_text}")
                    return None

            finally:
                driver.quit()

        except Exception as e:
            print(f"Error fetching Target price for {product_id}: {e}")
            return None

    def _extract_price(self, html: str) -> Optional[float]:
        """Not used - Selenium handles extraction directly in fetch_price."""
        _ = html
        return None


class WalgreensScraper(BaseScraper):
    """Scraper for Walgreens.com using Selenium."""

    def __init__(self):
        super().__init__("walgreens")

    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """Fetch current price from Walgreens using Selenium."""
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from webdriver_manager.firefox import GeckoDriverManager

            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--width=1920')
            firefox_options.add_argument('--height=1080')

            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

            try:
                driver.get(url)
                time.sleep(4)  # Walgreens needs extra time

                # Walgreens uses class-based selectors
                price_selectors = [
                    (By.CSS_SELECTOR, 'span.product__price'),
                    (By.CSS_SELECTOR, '[class*="price"]'),
                ]

                price_text = None
                for by, selector in price_selectors:
                    try:
                        element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((by, selector))
                        )
                        price_text = element.text
                        if '$' in price_text:
                            break
                    except:
                        continue

                if not price_text:
                    print(f"Could not find price for {product_id}")
                    return None

                price_match = re.search(r'\$?(\d+\.\d{2})', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    return PricePoint(
                        product_id=product_id,
                        retailer_id=self.retailer_id,
                        price=price,
                        timestamp=datetime.now(),
                        url=url
                    )
                else:
                    print(f"Could not parse price from: {price_text}")
                    return None

            finally:
                driver.quit()

        except Exception as e:
            print(f"Error fetching Walgreens price for {product_id}: {e}")
            return None

    def _extract_price(self, html: str) -> Optional[float]:
        """Not used - Selenium handles extraction."""
        _ = html
        return None


class AmazonScraper(BaseScraper):
    """Scraper for Amazon.com using Selenium."""

    def __init__(self):
        super().__init__("amazon")

    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """Fetch current price from Amazon using Selenium."""
        try:
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service
            from selenium.webdriver.firefox.options import Options
            from selenium.webdriver.common.by import By
            from webdriver_manager.firefox import GeckoDriverManager

            firefox_options = Options()
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--width=1920')
            firefox_options.add_argument('--height=1080')

            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)

            try:
                driver.get(url)
                time.sleep(5)  # Amazon needs more time

                # Amazon price selectors - try .get_attribute first
                price_selectors = [
                    (By.CSS_SELECTOR, 'span.a-price span.a-offscreen'),
                    (By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div .a-offscreen'),
                    (By.CSS_SELECTOR, 'span.a-price-whole'),
                    (By.CSS_SELECTOR, '#priceblock_ourprice'),
                    (By.CSS_SELECTOR, '#priceblock_dealprice'),
                ]

                price_text = None
                for by, selector in price_selectors:
                    try:
                        elements = driver.find_elements(by, selector)
                        for element in elements:
                            # Try both .text and .get_attribute
                            text = element.text or element.get_attribute('textContent') or ''
                            if text.strip() and ('$' in text or text.replace('.','').isdigit()):
                                price_text = text.strip()
                                break
                        if price_text:
                            break
                    except:
                        continue

                if not price_text:
                    print(f"Could not find price for {product_id}")
                    return None

                price_match = re.search(r'\$?(\d+\.\d{2})', price_text)
                if price_match:
                    price = float(price_match.group(1))
                    return PricePoint(
                        product_id=product_id,
                        retailer_id=self.retailer_id,
                        price=price,
                        timestamp=datetime.now(),
                        url=url
                    )
                else:
                    print(f"Could not parse price from: {price_text}")
                    return None

            finally:
                driver.quit()

        except Exception as e:
            print(f"Error fetching Amazon price for {product_id}: {e}")
            return None

    def _extract_price(self, html: str) -> Optional[float]:
        """Not used - Selenium handles extraction."""
        _ = html
        return None


class CVSScraper(BaseScraper):
    """
    Scraper for CVS.com using undetected-chromedriver.

    CVS has strong bot detection. This uses undetected-chromedriver to bypass it.

    Requirements:
    - Chrome browser installed
    - pip install undetected-chromedriver
    """

    def __init__(self):
        super().__init__("cvs")

    def fetch_price(self, product_id: str, url: str) -> Optional[PricePoint]:
        """
        Attempt to fetch price from CVS using undetected-chromedriver.

        Requires Chrome to be installed on the system.
        """
        try:
            import undetected_chromedriver as uc
            from selenium.webdriver.common.by import By

            # Check if Chrome is available
            try:
                options = uc.ChromeOptions()
                # NOTE: CVS blocks headless mode aggressively
                # Visible mode has 60-80% success vs 30-50% for headless
                # options.add_argument('--headless=new')  # Disabled: causes Access Denied
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--window-size=1920,1080')
                # Minimize the window to reduce distraction
                options.add_argument('--window-position=-2400,-2400')

                driver = uc.Chrome(options=options, use_subprocess=True)
            except Exception as e:
                print(f"[ERROR] Chrome not found. Please install Chrome first.")
                print(f"[ERROR] Details: {e}")
                print(f"[INFO] Download Chrome: https://www.google.com/chrome/")
                print(f"[INFO] Use ManualPriceEntry for: {product_id}")
                return None

            try:
                driver.get(url)
                time.sleep(8)  # CVS needs time to load and render price

                # Check if we got blocked
                page_title = driver.title
                if 'Access Denied' in page_title or 'denied' in page_title.lower():
                    print(f"[BLOCKED] CVS blocked the request (got '{page_title}')")
                    print(f"[INFO] This is expected ~40% of the time. Retry or use visible mode.")
                    return None

                # Extract all visible text from the page
                body = driver.find_element(By.TAG_NAME, 'body')
                all_text = body.text

                # Find all prices in format $XX.XX
                price_matches = re.findall(r'\$(\d+)\.(\d{2})', all_text)

                if not price_matches:
                    print(f"Could not find price for {product_id}")
                    print(f"[INFO] Page loaded but no prices found")
                    return None

                # The main product price is typically the first significant price
                # Filter out $0.00 and very small prices
                significant_prices = [
                    (dollars, cents) for dollars, cents in price_matches
                    if int(dollars) > 0 or int(cents) > 0
                ]

                if not significant_prices:
                    print(f"No significant prices found (all were $0.00)")
                    return None

                dollars, cents = significant_prices[0]
                price = float(f"{dollars}.{cents}")

                print(f"[SUCCESS] Found price: ${price:.2f}")
                return PricePoint(
                    product_id=product_id,
                    retailer_id=self.retailer_id,
                    price=price,
                    timestamp=datetime.now(),
                    url=url
                )

            finally:
                driver.quit()

        except ImportError:
            print(f"[ERROR] undetected-chromedriver not installed")
            print(f"[INFO] Install: pip install undetected-chromedriver")
            print(f"[INFO] Use ManualPriceEntry for: {product_id}")
            return None
        except Exception as e:
            print(f"Error fetching CVS price for {product_id}: {e}")
            return None

    def _extract_price(self, html: str) -> Optional[float]:
        """Not used - Selenium handles extraction."""
        _ = html
        return None


class ManualPriceEntry:
    """
    Helper for manual price entry during prototype phase.
    Use this until you have working scrapers.
    """
    
    @staticmethod
    def create_price_point(
        product_id: str,
        retailer_id: str,
        price: float,
        url: str,
        pack_size: int = 1,
        advertised_savings: Optional[float] = None
    ) -> PricePoint:
        """Create a price point from manual entry."""
        return PricePoint(
            product_id=product_id,
            retailer_id=retailer_id,
            price=price,
            timestamp=datetime.now(),
            url=url,
            pack_size=pack_size,
            advertised_savings=advertised_savings
        )
    
    @staticmethod
    def interactive_entry() -> PricePoint:
        """Interactive CLI for entering a price point."""
        print("\n=== Manual Price Entry ===")
        product_id = input("Product ID: ")
        retailer_id = input("Retailer ID (walmart/target): ")
        price = float(input("Price: $"))
        url = input("Product URL: ")
        pack_size = int(input("Pack size (1 for single): ") or "1")
        
        savings_input = input("Advertised savings (leave empty if none): $")
        advertised_savings = float(savings_input) if savings_input else None
        
        return ManualPriceEntry.create_price_point(
            product_id=product_id,
            retailer_id=retailer_id,
            price=price,
            url=url,
            pack_size=pack_size,
            advertised_savings=advertised_savings
        )


# Example usage for when you implement real scrapers:
"""
from scraper import WalmartScraper, TargetScraper

walmart = WalmartScraper()
target = TargetScraper()

# Fetch prices
walmart_price = walmart.fetch_price(
    product_id="eucerin-eczema-5oz",
    url="https://www.walmart.com/ip/..."
)

if walmart_price:
    db.add_price_point(walmart_price)
"""
