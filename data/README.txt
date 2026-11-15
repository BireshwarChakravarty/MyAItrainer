PRACTICE DATA PACK - AI for Procurement & Warehouse Auditing
All companies, people and numbers are invented for training. Nothing here is real.

Scenario: a distributor with 7 warehouses (WH01-WH07). Period: August to October 2026.
Snapshot date for stock and open items: 31 October 2026. Dates are YYYY-MM-DD.
Rules: count tolerance is +/-2% per line. PO approval limit is $5,000 (manager) and $20,000 (director).
Variance = counted quantity minus system quantity (negative = stock missing).

FILES
cycle_counts.csv     October cycle counts. Unit_Cost is per EA. Case_Size = units per case.
po_register.csv      Purchase orders (one line each). Order_UOM EA or CS (case). Promised_Date = agreed delivery date.
grn_register.csv     Goods receipts against POs. UOM is the unit the receipt was posted in.
invoice_register.csv Supplier invoices. Blank PO_No = invoice without a purchase order.
vendor_master.csv    Supplier records. Bank_Last4 is masked. Last_Transaction = latest invoice date.
transfers.csv        Inter-warehouse transfers. Blank Receipt_Date = not yet received.
stock_on_hand.csv    Stock by warehouse at 31 Oct 2026, with last movement date and average monthly usage.
spend_lines.csv      Indirect (non-stock) spend lines from accounts payable, Jul-Sep 2026, with messy descriptions.

Each file contains deliberate problems for you to find. Try the course assignments before reading ANSWER_KEY.md.
