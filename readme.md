# SuperBudget

## Formatting

Standard: YYYY_MM_DD Vendor FreeText Purchaser

- (FreeText can be anything, normally Order ID, receipt number, or description)

Manual (if parsing error) YYYY_MM_DD Vendor FreeText Purchaser$dd_cc

- (dd=dollar, cc=cent)

Examples:
2022_03_31 Dominos Lunch Tayler

2022_01_24 FIRSTChoice Order_CH143255 Tayler$54_93

### income.csv

| sponsor | amount |
|---------|--------|

#### Keyword

CarryOver = Previous year's balance

### vendor_category.csv

| vendor | category |
|--------|----------|
