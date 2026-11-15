# Answer key: practice data pack

Do the course assignments before reading this. All data is fictional.

## Cycle counts (cycle_counts.csv)
- Rows: 829 (the same rows are split by warehouse in warehouse_files.zip; WH04's file has a title row above the headers). Lines outside ±2% tolerance: 54. Network accuracy: 93.5%.
- Accuracy by warehouse: WH01 96.7%, WH02 95.8%, WH03 92.3%, WH04 95.5%, WH05 87.1%, WH06 94.7%, WH07 94.0%. Lowest: WH05.
- Gross variance value: $181,984.37; net: $-13,405.37.
- Gross by warehouse: WH01 $11,092.42, WH02 $41,448.73, WH03 $15,898.34, WH04 $30,757.09, WH05 $19,216.16, WH06 $41,347.57, WH07 $22,224.06.
- Planted issues:
  - Unit-of-measure errors: 14 out-of-tolerance lines whose variance is an exact multiple of the case size, concentrated in WH05.
  - Counter C17 at WH03: 9 of 30 WH03 lines outside tolerance.
  - Mis-slot at WH04: SKU-10219 short 40 in A-12-03 and over 40 in A-21-03 (nets to zero).
  - Unposted transfers: SKU-10126, SKU-10173, SKU-10216 short in WH02 and over by the same quantity in WH06, with no transfer record.
  - Genuine high-value shortages at WH07 on A-class items: SKU-10161, SKU-10176, SKU-10170, SKU-10165.

## Purchasing and payables
- Invoice register: 430 rows, total Amount $1,252,116.54.
- POs: 422. Split-PO clusters: 4, all by requester R07 at WH03 (11 POs, $52,331.94 in total).
- Near-duplicate invoices: 5 pairs worth $26,099.91 (duplicate refs: AP00420, AP00421, AP00422, AP00423, AP00424). Patterns: letter suffix, leading zeros and dashes, transposed digits, same invoice under duplicate vendor V049, same amount a few days apart.
- Invoices without a PO: 6 totalling $51,950.00; three are from new vendor V051 ($43,950.00).
- Invoice quantity above goods received: AP00322, AP00193, AP00153, AP00020.
- Invoice price more than 2% above PO: AP00228, AP00168, AP00351, AP00359, AP00117.
- Invoice dated before its PO: AP00118, AP00398.
- Unit-of-measure receipt: PO-70422 ordered 10 CS, receipted as 120 EA.

## Vendor master
- Records: 51. Duplicate pairs: V009/V049 (same tax ID and bank), V022/V050 (same name once standardised, same tax ID), V015/V044 (same bank and phone).
- Missing tax ID: 5. Dormant (no transaction for 18 months to 31 Oct 2026): 7.
- New vendor V051: created 22 Sep 2026, PO Box address, no tax ID, $43,950.00 invoiced without POs.

## Transfers, stock health, suppliers, spend
- Transfers not received after 14+ days: 5 (TR-4100, TR-4061, TR-4074, TR-4078, TR-4077). Received short: 3.
- Stock on hand $12,262,591.38; no movement for over 365 days: 34 lines worth $539,007.21, most in WH07. Lines with more than 12 months of supply: 26.
- OTIF (on time, in full, right unit) overall 88.1%; worst supplier V012 at 31.2%.
- Indirect spend $645,160.91 across 154 lines; largest category Temporary labour; coded to 6999 Sundry: $161,600.14.
- Spend by category: Temporary labour $145,300.58; Utilities $118,711.69; Facility services $84,947.59; Freight & courier $84,182.46; MHE maintenance & parts $81,046.40; IT & telecoms $55,209.49; Packaging materials $46,251.75; PPE & safety $29,510.95.
