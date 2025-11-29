# Database-Driven Price Collection

## Overview

The price tracking system now stores product information (including retailer URLs) in the database, enabling automated price collection without hardcoded URLs.

## Database Schema

### Products Table
- `id` - Internal product ID (e.g., "eucerin-advanced-repair-lotion-16.9oz")
- `name` - Product name
- `size` - Product size (e.g., "16.9 oz")
- `category` - Product category (e.g., "skincare")
- `upc` - Universal Product Code
- `target_url` - Product URL at Target
- `walmart_url` - Product URL at Walmart
- `cvs_url` - Product URL at CVS
- `walgreens_url` - Product URL at Walgreens
- `amazon_url` - Product URL at Amazon
- `created_at` - Timestamp when product was added
- `updated_at` - Timestamp when product was last updated

## Scripts

### 1. Migration Script
**File**: `migrate_add_product_urls.py`

Migrates the database to add retailer URL columns and inserts the first product.

```bash
python3 migrate_add_product_urls.py
```

**What it does**:
- Adds new columns to products table (if needed)
- Inserts Eucerin Advanced Repair Lotion with all 5 retailer URLs
- Verifies the migration was successful

### 2. Price Collection Script
**File**: `collect_prices.py`

Automated price collection from all configured retailers.

```bash
# Collect prices for all products
python3 collect_prices.py

# Collect prices for a specific product
python3 collect_prices.py eucerin-advanced-repair-lotion-16.9oz
```

**Features**:
- Reads products from database
- Automatically scrapes all retailers with configured URLs
- Saves price points to database
- Provides detailed progress and summary

### 3. View Prices Script
**File**: `view_prices.py`

Display collected price history from the database.

```bash
python3 view_prices.py
```

**Output**:
- Shows all products
- Lists recent prices for each retailer
- Displays timestamps for each price point

## Current Product

### Eucerin Advanced Repair Lotion (16.9 oz)
- **Product ID**: `eucerin-advanced-repair-lotion-16.9oz`
- **UPC**: `072140634827`
- **Category**: skincare

**Configured URLs**:
- ✓ Target
- ✓ Walmart
- ✓ CVS
- ✓ Walgreens
- ✓ Amazon

## Adding New Products

To add a new product, create a script or use Python:

```python
from src.database import PriceDatabase
from src.models import Product

db = PriceDatabase()

new_product = Product(
    id="product-slug",
    name="Product Name",
    size="Size",
    category="category",
    upc="123456789012",
    target_url="https://...",
    walmart_url="https://...",
    cvs_url="https://...",
    walgreens_url="https://...",
    amazon_url="https://..."
)

db.add_product(new_product)
db.close()
```

## Latest Test Results

**Eucerin Advanced Repair Lotion** (collected Nov 29, 2025):
- Target: $12.99 ✓
- CVS: $15.79 ✓
- Walgreens: $11.49 ✓
- Amazon: $9.74 ✓ (Best price!)
- Walmart: Failed (1 failure)

**Success Rate**: 4/5 (80%)

## Next Steps

1. **Set up automated collection** - Create cron job to run `collect_prices.py` daily
2. **Add more products** - Expand to track additional products
3. **Implement alerts** - Notify when prices drop below thresholds
4. **Add sale price detection** - Track both regular and sale prices
5. **Create dashboard** - Build web interface to view prices

## Files Modified

- `src/models.py` - Added retailer URL fields to Product model
- `src/database.py` - Updated schema and methods for new fields
- `migrate_add_product_urls.py` - Database migration script
- `collect_prices.py` - Automated collection script
- `view_prices.py` - Price viewing utility

## Benefits

✅ **No hardcoded URLs** - All URLs stored in database
✅ **Easy to add products** - Simple Product object creation
✅ **Automated collection** - Run once, scrape all retailers
✅ **Historical tracking** - All prices saved to database
✅ **Scalable** - Add unlimited products without code changes
