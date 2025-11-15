# Price History Companion (Concept)

Standalone comparison module for showing simple price history and current pricing on a small set of products across major retailers (e.g., Target, Amazon, Walmart). Intended to live inside a website or app, not as the primary product.

## Goal

Help specific user groups (e.g., people with reactive skin / eczema / chronic dryness) quickly see:

- How prices for key products move over time
- Whether a “deal” is real or just framed as savings
- Which retailer tends to be most consistent or fair on pricing

## Core Idea

For a small, curated product set (e.g. Eucerin Eczema Repair, Pataday Maximum Strength, etc.):

- Pull **current** prices from 3 major retailers  
- Store / fetch **historical** prices to show simple trends  
- Present **side-by-side comparison** for each product:
  - Current price per retailer
  - “Deal” flag vs historical average (is this actually cheaper?)
  - Simple visualization of recent price trend (e.g., 7 / 30 / 90 days)

## Example Use Case

- Product: **Pataday Maximum Strength**  
- Retailer A (Walmart): 2-pack at “$42 instead of $44” (advertised $2 savings)  
- Retailer B (Walmart, single): 1-pack at ~$20  
- Retailer C (Amazon): 2-pack around ~$23  

The module would:

- Show all options together (per-unit or per-pack normalization)
- Indicate when “$1 off” or “$2 off” claims are misleading compared to other retailers
- Highlight odd cases that might be **price mistakes** or **shipping-driven pricing**

## Intended Output

For each product:

- Compact card or table with:
  - Product name + size (e.g., 5 oz, 2x2.5 mL)
  - Current prices at Target / Amazon / Walmart
  - Historical min / max / average
  - Simple trend indicator (up, down, stable) over selected timeframe

## Constraints / Challenges (Notes to Self)

- Getting reliable **historical price data** from each retailer
- Dealing with:
  - Package size differences (single vs 2-pack)
  - Regional or membership pricing
  - Shipping vs pickup vs in-store price
- Keeping the product list small and curated to stay manageable

## Repo Purpose

This repo is **idea + prototype notes** for:

- Data model and interfaces for a “Price History Companion” module  
- Potential UI sketches for embedding in an app/site  
- Experiments with fetching, storing, and displaying multi-retailer price history
