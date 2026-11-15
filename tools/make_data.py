"""Generate the fictional practice data pack for the course.

All companies, people and figures are invented. Issues are planted deliberately
so learners can find them, and the true answers are computed here and written to
src/95-answers.html (used by the auto-checked assignments) and data/ANSWER_KEY.md.

Run:  python3 tools/make_data.py
"""
import csv, json, random, zipfile, datetime as dt
from collections import defaultdict
from pathlib import Path

random.seed(20261101)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
D = dt.date
def iso(d): return d.isoformat() if d else ""
def rdate(a, b): return a + dt.timedelta(days=random.randint(0, (b - a).days))

WH = [("WH01", "Central DC"), ("WH02", "North"), ("WH03", "East"), ("WH04", "South"),
      ("WH05", "Port"), ("WH06", "West"), ("WH07", "Cold Store")]
WHC = [w for w, _ in WH]
TOL = 0.02
LIMIT = 5000

# ---------------- SKUs ----------------
CATS = {
 "Stretch film": (18, 60, [1, 6]), "Carton": (0.6, 3.5, [12, 24]), "Pallet": (9, 24, [1]),
 "Label roll": (4, 15, [6, 12]), "Tape": (1.2, 4, [12, 24]), "Bearing": (14, 120, [1]),
 "Drive belt": (22, 140, [1]), "Hydraulic oil 20L": (60, 110, [1]), "Safety gloves": (2, 6, [12]),
 "Hi-vis vest": (4, 9, [12]), "Barcode scanner": (380, 950, [1]), "Battery pack": (240, 620, [1]),
 "Chilled tote": (12, 30, [6]), "Pallet wrap net": (25, 70, [1]), "Desiccant pack": (0.3, 1.2, [24]),
}
SKUS = []
n = 10001
for cat, (lo, hi, cases) in CATS.items():
    for i in range(16):
        cost = round(random.uniform(lo, hi), 2)
        SKUS.append(dict(SKU=f"SKU-{n}", Description=f"{cat} type {chr(65+i%8)}{i+1}",
                         Case_Size=random.choice(cases), Unit_Cost=cost,
                         usage=random.randint(5, 400)))
        n += 1
# ABC by annual value
for s in SKUS: s["annual"] = s["Unit_Cost"] * s["usage"] * 12
tot = sum(s["annual"] for s in SKUS); run = 0
for s in sorted(SKUS, key=lambda x: -x["annual"]):
    run += s["annual"]; s["ABC"] = "A" if run / tot <= .8 else ("B" if run / tot <= .95 else "C")
BYSKU = {s["SKU"]: s for s in SKUS}

# ---------------- vendors ----------------
PRE = ["Northline", "Ridgeway", "Harborview", "Summitpack", "Crestfield", "Bluegate", "Ironbridge", "Westmoor",
       "Kestrel", "Oakhurst", "Silverline", "Redbrook", "Granitefold", "Meridian", "Lakeshore", "Pinecrest",
       "Stonegate", "Fairmont", "Brightwater", "Copperfield", "Highmoor", "Riverbend", "Eastbrook", "Falconridge",
       "Sterlingworth", "Ashcombe", "Thornbury", "Wexley", "Calderon", "Marlowe", "Hollins", "Dunmore",
       "Kingsway", "Larchmont", "Moorfield", "Newhaven", "Orchard Lane", "Penrose", "Quayside", "Rosewood",
       "Saltmarsh", "Tallis", "Upland", "Vantage", "Whitcombe", "Yardley", "Zephyr Hill", "Beacon"]
SUF = ["Pallets", "Packaging", "Logistics", "Supplies", "Industrial", "Freight", "Services", "Equipment",
       "Plastics", "Labels", "Safety", "Facilities"]
LEG = ["Ltd", "Limited", "Co.", "Inc", "LLC"]
CITIES = ["Ashford", "Brookton", "Carlow", "Denby", "Elmstead", "Farley", "Greystone", "Halden"]
VEND = []
for i, p in enumerate(PRE):
    vid = f"V{i+1:03d}"
    VEND.append(dict(Vendor_ID=vid, Vendor_Name=f"{p} {random.choice(SUF)} {random.choice(LEG)}",
        Address=f"{random.randint(2,240)} {random.choice(['Mill','Station','Dock','Quarry','Park','Canal'])} Road",
        City=random.choice(CITIES), Tax_ID=f"TX{random.randint(1000000,9999999)}",
        Bank_Last4=f"{random.randint(1000,9999)}", Phone=f"0{random.randint(1000,1999)} {random.randint(100000,999999)}",
        Created_Date=iso(rdate(D(2015,1,1), D(2024,6,30))), Status="Active"))
V = {v["Vendor_ID"]: v for v in VEND}
V["V009"]["Vendor_Name"] = "Northline Pallets Ltd"
# planted vendor-master issues
dup_a = dict(V["V009"]); dup_a.update(Vendor_ID="V049", Vendor_Name="North Line Pallet Limited",
             Address=V["V009"]["Address"].upper(), Created_Date="2025-11-03")
V["V022"]["Vendor_Name"] = "Ridgeway Packaging Co."
dup_b = dict(V["V022"]); dup_b.update(Vendor_ID="V050", Vendor_Name="RIDGEWAY PACKAGING CO",
             Tax_ID=V["V022"]["Tax_ID"], Bank_Last4=f"{random.randint(1000,9999)}", Created_Date="2026-02-17")
V["V044"]["Bank_Last4"] = V["V015"]["Bank_Last4"]; V["V044"]["Phone"] = V["V015"]["Phone"]
newv = dict(Vendor_ID="V051", Vendor_Name="Apex Facility Solutions LLC", Address="PO Box 4471", City="Denby",
            Tax_ID="", Bank_Last4="8820", Phone="0700 555012", Created_Date="2026-09-22", Status="Active")
for vid in ["V004", "V027", "V033", "V038"]: V[vid]["Tax_ID"] = ""
VEND += [dup_a, dup_b, newv]
V = {v["Vendor_ID"]: v for v in VEND}
DORMANT = ["V005", "V017", "V024", "V029", "V036", "V041", "V046"]
SLOW_VENDOR = "V012"
ACTIVE_SUPPLY = [v for v in V if v not in DORMANT + ["V049", "V050", "V051", "V044"]]

# ---------------- cycle counts ----------------
counts = []; cid = 1
def add_count(w, s, sysq, cnt, loc=None, counter=None, day=None):
    global cid
    counts.append(dict(Count_ID=f"CC{cid:05d}", Count_Date=iso(day or D(2026,10,random.randint(1,30))),
        WH=w, Location=loc or f"{random.choice('ABCDEF')}-{random.randint(1,30):02d}-{random.randint(1,5):02d}",
        SKU=s["SKU"], Description=s["Description"], UOM="EA", Case_Size=s["Case_Size"], ABC=s["ABC"],
        Unit_Cost=s["Unit_Cost"], Sys_Qty=sysq, Cnt_Qty=cnt,
        Counter_ID=counter or f"C{random.randint(1,24):02d}"))
    cid += 1
def clean_qty(): return random.randint(40, 600)
lines = {"WH01": 120, "WH02": 115, "WH03": 120, "WH04": 110, "WH05": 125, "WH06": 110, "WH07": 80}
case_skus = [s for s in SKUS if s["Case_Size"] > 1]
single = [s for s in SKUS if s["Case_Size"] == 1]
A_high = sorted([s for s in single if s["ABC"] == "A"], key=lambda x: -x["Unit_Cost"])[:6]
plants = defaultdict(list)
for w in WHC:
    k = lines[w]; pool = random.sample(SKUS, k)
    errs = {"WH01": 4, "WH02": 2, "WH03": 2, "WH04": 3, "WH05": 4, "WH06": 3, "WH07": 1}[w]
    for i, s in enumerate(pool):
        q = clean_qty()
        if i < errs:  # ordinary random error, kept off case multiples
            d = random.choice([-1, 1]) * random.randint(max(4, int(q*.04)), max(6, int(q*.12)))
            if s["Case_Size"] > 1 and d % s["Case_Size"] == 0: d += 1
            add_count(w, s, q, max(0, q + d))
        else:
            noise = random.choice([0]*12 + [-1, 1]) if q >= 100 else 0
            add_count(w, s, q, q + noise)
# WH02/WH06 unposted transfers: WH02 short, WH06 over, same SKUs
for s in random.sample(single, 3):
    q = random.randint(30, 90)
    add_count("WH02", s, q + 200, 200, day=D(2026,10,14)); plants["transit"].append(s["SKU"])
    add_count("WH06", s, 50, 50 + q, day=D(2026,10,15))
# WH03 counter C17 errors
for s in random.sample(single, 9):
    q = random.randint(80, 300); d = random.choice([-1,1]) * random.randint(int(q*.05), int(q*.15))
    add_count("WH03", s, q, q + d, counter="C17")
for s in random.sample(SKUS, 14):
    q = random.randint(80, 300); add_count("WH03", s, q, q, counter="C17")
# WH04 mis-slot pair
ms = random.choice(single)
add_count("WH04", ms, 120, 80, loc="A-12-03", day=D(2026,10,9)); add_count("WH04", ms, 0, 40, loc="A-21-03", day=D(2026,10,9))
plants["misslot"] = ms["SKU"]
# WH05 UOM errors (variance exact multiple of case size)
for s in random.sample(case_skus, 14):
    q = random.randint(4, 20) * s["Case_Size"]; d = random.choice([-1,1]) * random.randint(1,3) * s["Case_Size"]
    if abs(d) / q <= TOL: d = d * 3
    add_count("WH05", s, q, max(0, q + d)); plants["uom"].append(s["SKU"])
# WH07 genuine high-value shortages
for s in A_high[:4]:
    q = random.randint(20, 45); add_count("WH07", s, q, q - random.randint(4, 8)); plants["hv"].append(s["SKU"])
random.shuffle(counts)
for i, r in enumerate(sorted(counts, key=lambda r: (r["WH"], r["Count_Date"]))): r["Count_ID"] = f"CC{i+1:05d}"
counts.sort(key=lambda r: r["Count_ID"])

def var_rows():
    out = []
    for r in counts:
        vq = r["Cnt_Qty"] - r["Sys_Qty"]
        vp = (0 if r["Cnt_Qty"] == 0 else 1) if r["Sys_Qty"] == 0 else vq / r["Sys_Qty"]
        out.append(dict(r, vq=vq, vp=vp, vv=round(vq * r["Unit_Cost"], 2), oot=abs(vp) > TOL))
    return out
VR = var_rows()

# ---------------- POs, GRNs, invoices ----------------
REQ = [f"R{i:02d}" for i in range(1, 11)]
def approver(v): return "D01" if v >= 20000 else ("M0" + str(random.randint(1, 4)) if v >= LIMIT else "Auto")
pos = []; pon = 70001
def add_po(day, w, vid, req, s, qty, price, uom="EA", promised=None):
    global pon
    val = round(qty * price, 2)
    pos.append(dict(PO_No=f"PO-{pon}", PO_Date=iso(day), WH=w, Vendor_ID=vid, Requester=req, SKU=s["SKU"],
        Order_UOM=uom, Qty=qty, Unit_Price=price, PO_Value=val,
        Promised_Date=iso(promised or day + dt.timedelta(days=random.randint(5, 14))), Approver=approver(val)))
    pon += 1; return pos[-1]
VSKU = {v: random.sample(SKUS, 8) for v in ACTIVE_SUPPLY}
for _ in range(400):
    vid = random.choice(ACTIVE_SUPPLY); s = random.choice(VSKU[vid])
    target = random.lognormvariate(7.4, 0.95)
    price = round(s["Unit_Cost"] * random.uniform(0.98, 1.05), 2)
    qty = max(1, int(target / price))
    add_po(rdate(D(2026,8,1), D(2026,10,20)), random.choice(WHC), vid, random.choice(REQ), s, qty, price)
# remove accidental split clusters among baseline
def clusters(rows):
    g = defaultdict(list)
    for p in rows:
        if p["PO_Value"] < LIMIT: g[(p["Vendor_ID"], p["Requester"])].append(p)
    found = []
    for key, ps in g.items():
        ps.sort(key=lambda p: p["PO_Date"]); i = 0
        while i < len(ps):
            grp = [ps[i]]; j = i + 1
            while j < len(ps) and (D.fromisoformat(ps[j]["PO_Date"]) - D.fromisoformat(grp[0]["PO_Date"])).days <= 7:
                grp.append(ps[j]); j += 1
            if len(grp) > 1 and sum(p["PO_Value"] for p in grp) > LIMIT: found.append(grp); i = j
            else: i += 1
    return found
for _ in range(50):
    c = clusters(pos)
    if not c: break
    for grp in c:
        for p in grp[1:]:
            p["Requester"] = random.choice([r for r in REQ if r not in ("R07", p["Requester"])])
# make sure the slow supplier has enough orders to stand out
for _ in range(10):
    s = random.choice(VSKU[SLOW_VENDOR]); price = s["Unit_Cost"]
    add_po(rdate(D(2026,8,1), D(2026,10,10)), random.choice(WHC), SLOW_VENDOR, random.choice(["R01","R02","R04"]), s, max(1, int(random.uniform(500, 3000) / price)), price)
for _ in range(50):
    c = clusters(pos)
    if not c: break
    for grp in c:
        for p in grp[1:]:
            p["Requester"] = random.choice([r for r in REQ if r not in ("R07", p["Requester"])])
assert not clusters(pos)
# planted split clusters by R07
split_pos = []
for vid, day in [("V018", D(2026,8,12)), ("V018", D(2026,9,3)), ("V026", D(2026,9,22)), ("V026", D(2026,10,13))]:
    s = VSKU[vid][0]
    for k in range(random.choice([2, 3])):
        val = random.uniform(4600, 4990); price = s["Unit_Cost"]; qty = int(val / price)
        while qty * price >= LIMIT: qty -= 1
        split_pos.append(add_po(day + dt.timedelta(days=k), "WH03", vid, "R07", s, qty, price)["PO_No"])
# planted case-UOM PO
uom_sku = [s for s in case_skus if s["Case_Size"] == 12][0]
uom_po = add_po(D(2026,10,6), "WH07", "V019", "R03", uom_sku, 10, round(uom_sku["Unit_Cost"]*12, 2), uom="CS")
# GRNs
grns = []; gn = 50001
today = D(2026,10,31)
short_rcv = []
for p in pos:
    pdte = D.fromisoformat(p["PO_Date"]); prom = D.fromisoformat(p["Promised_Date"])
    if pdte > D(2026,10,22) and random.random() < .5: continue  # still open
    late = random.random() < (0.7 if p["Vendor_ID"] == SLOW_VENDOR else 0.05)
    gdate = prom + dt.timedelta(days=random.randint(2, 9)) if late else prom - dt.timedelta(days=random.randint(0, 3))
    if gdate > today: continue
    qty = p["Qty"]; uom = p["Order_UOM"]
    if p is uom_po: qty, uom = 120, "EA"
    elif random.random() < 0.02 and qty > 10: qty = int(qty * random.uniform(.8, .95)); short_rcv.append(p["PO_No"])
    grns.append(dict(GRN_No=f"GRN-{gn}", PO_No=p["PO_No"], GRN_Date=iso(gdate), WH=p["WH"], SKU=p["SKU"],
                     Qty_Received=qty, UOM=uom)); gn += 1
GRN = {g["PO_No"]: g for g in grns}
POD = {p["PO_No"]: p for p in pos}
# invoices
invs = []; ref = 1
def add_inv(vid, no, day, po, sku, qty, price, status="Paid"):
    global ref
    invs.append(dict(Invoice_Ref=f"AP{ref:05d}", Vendor_ID=vid, Invoice_No=no, Invoice_Date=iso(day), PO_No=po,
                     SKU=sku, Qty=qty, Unit_Price=price, Amount=round(qty * price, 2), Status=status)); ref += 1
    return invs[-1]
for g in grns:
    p = POD[g["PO_No"]]; day = D.fromisoformat(g["GRN_Date"]) + dt.timedelta(days=random.randint(0, 6))
    if day > today: day = today
    qty = p["Qty"]; price = p["Unit_Price"]
    add_inv(p["Vendor_ID"], f"{random.randint(10000, 99999)}", day, p["PO_No"], p["SKU"], qty, price,
            "Pending" if day > D(2026,10,24) else "Paid")
base = [i for i in invs if i["PO_No"] not in split_pos and i["PO_No"] != uom_po["PO_No"]]
random.shuffle(base)
over_qty = []; over_price = []
for inv in base[:4]:
    g = GRN[inv["PO_No"]]; inv["Qty"] = g["Qty_Received"] + max(2, int(g["Qty_Received"] * .08))
    inv["Amount"] = round(inv["Qty"] * inv["Unit_Price"], 2); over_qty.append(inv["Invoice_Ref"])
for inv in base[4:9]:
    inv["Unit_Price"] = round(inv["Unit_Price"] * random.uniform(1.05, 1.12), 2)
    inv["Amount"] = round(inv["Qty"] * inv["Unit_Price"], 2); over_price.append(inv["Invoice_Ref"])
for inv in base[9:11]:  # invoice dated before PO (after-the-fact PO)
    p = POD[inv["PO_No"]]; inv["Invoice_Date"] = iso(D.fromisoformat(p["PO_Date"]) - dt.timedelta(days=random.randint(3, 8)))
before_po = [i["Invoice_Ref"] for i in base[9:11]]
# near duplicates
dups = []
def dup_of(orig, newno, vid=None, shift=4, amount=None):
    d = add_inv(vid or orig["Vendor_ID"], newno, D.fromisoformat(orig["Invoice_Date"]) + dt.timedelta(days=shift),
                orig["PO_No"], orig["SKU"], orig["Qty"], orig["Unit_Price"])
    dups.append((orig["Invoice_Ref"], d["Invoice_Ref"])); return d
c = base[12:17]
c[0]["Invoice_No"] = "33071"; dup_of(c[0], "33071A")
c[1]["Invoice_No"] = "INV-00451"; dup_of(c[1], "451", shift=9)
c[2]["Invoice_No"] = "88213"; dup_of(c[2], "88231", shift=6)
c[3]["Vendor_ID"] = "V009"; c[3]["Invoice_No"] = "NP-2290"; dup_of(c[3], "NP-2290", vid="V049", shift=11)
c[4]["Invoice_No"] = "70114"; dup_of(c[4], "70119", shift=3)
dup_ids = [b for a, b in dups]
# invoices without PO
nopo = []
for vid, no, day, amt in [("V051", "AFS-1001", D(2026,10,2), 14250.00), ("V051", "AFS-1007", D(2026,10,16), 16800.00),
                          ("V051", "AFS-1012", D(2026,10,28), 12900.00), ("V011", "S-7781", D(2026,9,12), 1850.00),
                          ("V034", "C-2219", D(2026,8,28), 3750.00), ("V040", "9921", D(2026,10,7), 2400.00)]:
    nopo.append(add_inv(vid, no, day, "", "", 1, amt, "Paid" if day < D(2026,10,24) else "Pending")["Invoice_Ref"])
invs.sort(key=lambda r: r["Invoice_Date"])

# ---------------- transfers ----------------
transfers = []
for t in range(1, 121):
    a, b = random.sample(WHC, 2); s = random.choice(single); q = random.randint(10, 120)
    sd = rdate(D(2026,9,1), D(2026,10,28)); rd = sd + dt.timedelta(days=random.randint(1, 4))
    transfers.append(dict(Transfer_ID=f"TR-{4000+t}", Ship_Date=iso(sd), From_WH=a, To_WH=b, SKU=s["SKU"],
                          Qty_Shipped=q, Receipt_Date=iso(rd if rd <= today else None), Qty_Received=q if rd <= today else ""))
unrec = []; shortt = []
for t in random.sample([t for t in transfers if t["Ship_Date"] < "2026-10-12"], 8)[:5]:
    t["Receipt_Date"] = ""; t["Qty_Received"] = ""; unrec.append(t["Transfer_ID"])
for t in random.sample([t for t in transfers if t["Receipt_Date"] and t["Transfer_ID"] not in unrec], 3):
    t["Qty_Received"] = t["Qty_Shipped"] - random.randint(3, 9); shortt.append(t["Transfer_ID"])
open_recent = [t["Transfer_ID"] for t in transfers if not t["Receipt_Date"] and t["Transfer_ID"] not in unrec]
transfers.sort(key=lambda t: t["Transfer_ID"])

# ---------------- stock on hand ----------------
soh = []
for w in WHC:
    for s in random.sample(SKUS, 85):
        usage = max(2, int(s["usage"] * random.uniform(.05, .3)))
        q = max(5, int(usage * random.uniform(0.5, 9))); last = rdate(D(2026,7,1), D(2026,10,31))
        soh.append(dict(WH=w, SKU=s["SKU"], Description=s["Description"], Qty_On_Hand=q, Unit_Cost=s["Unit_Cost"],
                        Stock_Value=round(q * s["Unit_Cost"], 2), Last_Movement_Date=iso(last), Avg_Monthly_Usage=usage))
for r in random.sample(soh, 34):  # obsolete
    r["Last_Movement_Date"] = iso(rdate(D(2024,3,1), D(2025,9,30))); r["Avg_Monthly_Usage"] = 0
for r in random.sample([r for r in soh if r["Avg_Monthly_Usage"] > 0], 26):  # excess
    r["Qty_On_Hand"] = r["Avg_Monthly_Usage"] * random.randint(14, 30); r["Stock_Value"] = round(r["Qty_On_Hand"] * r["Unit_Cost"], 2)
soh.sort(key=lambda r: (r["WH"], r["SKU"]))

# ---------------- indirect spend lines ----------------
SP = {
 "Packaging materials": [("Ridgeway Packaging Co.", ["stretch wrap 23mic x {n} rolls", "cartons 600x400 dbl wall", "void fill paper", "tape 48mm brown x {n}"], (300, 4200))],
 "MHE maintenance & parts": [("Kestrel Equipment Inc", ["forklift service {m}", "reach truck repair - mast chain", "FLT tyres x {n}", "LOLER inspection"], (400, 6800))],
 "Facility services": [("Apex Facility Solutions LLC", ["cleaning contract {m}", "security guard cover {m}", "pest control visit", "waste skip exchange"], (500, 9000))],
 "Utilities": [("Eastbrook Services Ltd", ["electricity {m} WH0{w}", "water/sewer {m}", "gas {m}"], (900, 12000))],
 "Temporary labour": [("Dunmore Services Co.", ["agency pickers wk {wk}", "temp drivers wk {wk}", "peak cover {m}"], (1500, 14000))],
 "Freight & courier": [("Quayside Freight Ltd", ["inbound haulage {m}", "courier same day", "pallet network {m}", "fuel surcharge"], (200, 8000))],
 "IT & telecoms": [("Vantage Industrial LLC", ["scanner repairs x {n}", "wifi access points", "mobile data {m}", "label printer heads"], (150, 5200))],
 "PPE & safety": [("Saltmarsh Safety Ltd", ["safety boots x {n}", "hi-vis vests", "gloves cut resistant", "first aid restock"], (80, 2600))],
}
MONTHS = ["Jul", "Aug", "Sep"]
spend = []; ln = 1
for cat, opts in SP.items():
    for vname, descs, (lo, hi) in opts:
        for _ in range(random.randint(15, 24)):
            d = random.choice(descs).format(n=random.randint(2, 40), m=random.choice(MONTHS), w=random.randint(1, 7), wk=random.randint(27, 39))
            if random.random() < .3: d = d.upper()
            gl = random.choice(["6100 Repairs", "6200 Consumables", "6300 Services", "6999 Sundry"])
            spend.append(dict(Line_ID=f"SP{ln:04d}", Vendor_Name=vname, Description=d,
                              Amount=round(random.uniform(lo, hi), 2), GL_Code=gl, _cat=cat)); ln += 1
random.shuffle(spend)
for i, r in enumerate(spend): r["Line_ID"] = f"SP{i+1:04d}"

# ---------------- vendor last transaction ----------------
last = defaultdict(str)
for i in invs:
    last[i["Vendor_ID"]] = max(last[i["Vendor_ID"]], i["Invoice_Date"])
for v in VEND:
    if v["Vendor_ID"] in DORMANT: v["Last_Transaction"] = iso(rdate(D(2023,6,1), D(2025,3,31)))
    else: v["Last_Transaction"] = last.get(v["Vendor_ID"]) or iso(rdate(D(2025,12,1), D(2026,7,31)))
VEND.sort(key=lambda v: v["Vendor_ID"])

# ---------------- write files ----------------
def wcsv(name, rows, cols):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
FILES = {
 "cycle_counts.csv": (counts, ["Count_ID","Count_Date","WH","Location","SKU","Description","UOM","Case_Size","ABC","Unit_Cost","Sys_Qty","Cnt_Qty","Counter_ID"]),
 "po_register.csv": (pos, ["PO_No","PO_Date","WH","Vendor_ID","Requester","SKU","Order_UOM","Qty","Unit_Price","PO_Value","Promised_Date","Approver"]),
 "grn_register.csv": (grns, ["GRN_No","PO_No","GRN_Date","WH","SKU","Qty_Received","UOM"]),
 "invoice_register.csv": (invs, ["Invoice_Ref","Vendor_ID","Invoice_No","Invoice_Date","PO_No","SKU","Qty","Unit_Price","Amount","Status"]),
 "vendor_master.csv": (VEND, ["Vendor_ID","Vendor_Name","Address","City","Tax_ID","Bank_Last4","Phone","Created_Date","Status","Last_Transaction"]),
 "transfers.csv": (transfers, ["Transfer_ID","Ship_Date","From_WH","To_WH","SKU","Qty_Shipped","Receipt_Date","Qty_Received"]),
 "stock_on_hand.csv": (soh, ["WH","SKU","Description","Qty_On_Hand","Unit_Cost","Stock_Value","Last_Movement_Date","Avg_Monthly_Usage"]),
 "spend_lines.csv": (spend, ["Line_ID","Vendor_Name","Description","Amount","GL_Code"]),
}
for name, (rows, cols) in FILES.items(): wcsv(name, rows, cols)

README = """PRACTICE DATA PACK - AI for Procurement & Warehouse Auditing
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
"""
(OUT / "README.txt").write_text(README)

# Excel workbook
from openpyxl import Workbook
from openpyxl.styles import Font
wb = Workbook(); ws = wb.active; ws.title = "Read me"
for line in README.splitlines(): ws.append([line])
ws["A1"].font = Font(bold=True)
DATECOLS = {"Count_Date","PO_Date","Promised_Date","GRN_Date","Invoice_Date","Created_Date","Last_Transaction","Ship_Date","Receipt_Date","Last_Movement_Date"}
for name, (rows, cols) in FILES.items():
    sh = wb.create_sheet(name.replace(".csv", "")[:31]); sh.append(cols)
    for c in sh[1]: c.font = Font(bold=True)
    for r in rows:
        vals = []
        for c in cols:
            v = r.get(c, "")
            if c in DATECOLS and v: v = D.fromisoformat(v)
            vals.append(v)
        sh.append(vals)
    for col in sh.columns:
        sh.column_dimensions[col[0].column_letter].width = max(10, min(40, max(len(str(c.value or "")) for c in col) + 2))
    for c in cols:
        if c in DATECOLS:
            idx = cols.index(c) + 1
            for row in sh.iter_rows(min_row=2, min_col=idx, max_col=idx):
                row[0].number_format = "yyyy-mm-dd"
wb.save(OUT / "practice_pack.xlsx")

# ---------------- answers ----------------
A = {}
byw = defaultdict(list)
for r in VR: byw[r["WH"]].append(r)
A["count_rows"] = len(VR)
A["oot_lines"] = sum(r["oot"] for r in VR)
A["ira"] = {w: round(100 * sum(not r["oot"] for r in byw[w]) / len(byw[w]), 1) for w in WHC}
A["network_ira"] = round(100 * sum(not r["oot"] for r in VR) / len(VR), 1)
A["gross_var"] = {w: round(sum(abs(r["vv"]) for r in byw[w]), 2) for w in WHC}
A["net_var"] = {w: round(sum(r["vv"] for r in byw[w]), 2) for w in WHC}
A["gross_total"] = round(sum(abs(r["vv"]) for r in VR), 2)
A["net_total"] = round(sum(r["vv"] for r in VR), 2)
A["lowest_wh"] = min(WHC, key=lambda w: A["ira"][w])
A["uom_lines"] = sum(1 for r in VR if r["oot"] and r["Case_Size"] > 1 and r["vq"] != 0 and r["vq"] % r["Case_Size"] == 0)
A["uom_wh"] = max(WHC, key=lambda w: sum(1 for r in byw[w] if r["oot"] and r["Case_Size"] > 1 and r["vq"] % r["Case_Size"] == 0))
c17 = [r for r in VR if r["Counter_ID"] == "C17" and r["WH"] == "WH03"]
A["counter_worst"] = "C17"; A["c17_lines"] = len(c17); A["c17_oot"] = sum(r["oot"] for r in c17)
A["misslot_sku"] = plants["misslot"]; A["transit_skus"] = plants["transit"]; A["hv_skus"] = plants["hv"]
A["wh07_gross"] = A["gross_var"]["WH07"]
A["po_rows"] = len(pos); A["split_requester"] = "R07"; A["split_po_count"] = len(split_pos)
cl = clusters(pos); A["split_clusters"] = len(cl)
A["split_total"] = round(sum(POD[p]["PO_Value"] for p in split_pos), 2)
A["dup_pairs"] = len(dups); A["dup_value"] = round(sum(next(i for i in invs if i["Invoice_Ref"] == b)["Amount"] for a, b in dups), 2)
A["nopo_count"] = len(nopo); A["nopo_total"] = round(sum(next(i for i in invs if i["Invoice_Ref"] == r)["Amount"] for r in nopo), 2)
A["over_qty"] = over_qty; A["over_price"] = over_price; A["before_po"] = before_po
A["uom_po"] = uom_po["PO_No"]
A["vendor_rows"] = len(VEND); A["vendor_missing_tax"] = sum(1 for v in VEND if not v["Tax_ID"])
A["vendor_dormant"] = sum(1 for v in VEND if v["Last_Transaction"] < "2025-04-30")
A["vendor_dup_pairs"] = 3; A["new_vendor"] = "V051"
A["new_vendor_paid"] = round(sum(i["Amount"] for i in invs if i["Vendor_ID"] == "V051"), 2)
A["transfers_unreceived_14d"] = len(unrec); A["transfers_short"] = len(shortt)
A["transfers_unrec_ids"] = unrec
for r in soh:
    r["_age"] = (today - D.fromisoformat(r["Last_Movement_Date"])).days
A["soh_rows"] = len(soh); A["soh_value"] = round(sum(r["Stock_Value"] for r in soh), 2)
A["aged365_value"] = round(sum(r["Stock_Value"] for r in soh if r["_age"] > 365), 2)
A["aged365_lines"] = sum(1 for r in soh if r["_age"] > 365)
aged_w = defaultdict(float)
for r in soh:
    if r["_age"] > 365: aged_w[r["WH"]] += r["Stock_Value"]
A["aged365_top_wh"] = max(aged_w, key=aged_w.get)
A["excess_lines"] = sum(1 for r in soh if r["Avg_Monthly_Usage"] > 0 and r["Qty_On_Hand"] / r["Avg_Monthly_Usage"] > 12)
# OTIF by vendor
ot = defaultdict(lambda: [0, 0])
for p in pos:
    g = GRN.get(p["PO_No"])
    if not g: continue
    ok = g["GRN_Date"] <= p["Promised_Date"] and g["Qty_Received"] >= p["Qty"] and g["UOM"] == p["Order_UOM"]
    ot[p["Vendor_ID"]][0] += ok; ot[p["Vendor_ID"]][1] += 1
otif = {v: round(100 * a / b, 1) for v, (a, b) in ot.items() if b >= 5}
A["otif_worst"] = min(otif, key=otif.get); A["otif_worst_pct"] = otif[A["otif_worst"]]
A["otif_overall"] = round(100 * sum(a for a, b in ot.values()) / sum(b for a, b in ot.values()), 1)
cat_tot = defaultdict(float)
for r in spend: cat_tot[r["_cat"]] += r["Amount"]
A["spend_total"] = round(sum(r["Amount"] for r in spend), 2)
A["spend_top_cat"] = max(cat_tot, key=cat_tot.get)
A["spend_by_cat"] = {k: round(v, 2) for k, v in sorted(cat_tot.items(), key=lambda x: -x[1])}
A["spend_sundry"] = round(sum(r["Amount"] for r in spend if r["GL_Code"].startswith("6999")), 2)
A["spend_lines"] = len(spend)
A["invoice_total"] = round(sum(i["Amount"] for i in invs), 2)
A["invoice_rows"] = len(invs)
A["dup_refs"] = dup_ids
A["otif_by_vendor"] = otif

# per-warehouse count files for the Power Query exercise (WH04's has a title row above the headers)
wf = OUT / "warehouse_files"; wf.mkdir(exist_ok=True)
cc_cols = FILES["cycle_counts.csv"][1]
for w in WHC:
    wbw = Workbook(); sh = wbw.active; sh.title = "Counts"
    if w == "WH04": sh.append([f"{w} South - October 2026 cycle counts"]); sh.append([])
    sh.append(cc_cols)
    for r in counts:
        if r["WH"] == w: sh.append([D.fromisoformat(r[c]) if c == "Count_Date" else r[c] for c in cc_cols])
    wbw.save(wf / f"{w}_counts_Oct2026.xlsx")
with zipfile.ZipFile(OUT / "warehouse_files.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for w in WHC: z.write(wf / f"{w}_counts_Oct2026.xlsx", f"warehouse_files/{w}_counts_Oct2026.xlsx")

(ROOT / "src" / "95-answers.html").write_text("<script>window.PRACTICE=" + json.dumps(A) + ";</script>\n")

def money(x): return f"${x:,.2f}"
key = f"""# Answer key: practice data pack

Do the course assignments before reading this. All data is fictional.

## Cycle counts (cycle_counts.csv)
- Rows: {A['count_rows']} (the same rows are split by warehouse in warehouse_files.zip; WH04's file has a title row above the headers). Lines outside ±2% tolerance: {A['oot_lines']}. Network accuracy: {A['network_ira']}%.
- Accuracy by warehouse: {', '.join(f"{w} {A['ira'][w]}%" for w in WHC)}. Lowest: {A['lowest_wh']}.
- Gross variance value: {money(A['gross_total'])}; net: {money(A['net_total'])}.
- Gross by warehouse: {', '.join(f"{w} {money(A['gross_var'][w])}" for w in WHC)}.
- Planted issues:
  - Unit-of-measure errors: {A['uom_lines']} out-of-tolerance lines whose variance is an exact multiple of the case size, concentrated in {A['uom_wh']}.
  - Counter C17 at WH03: {A["c17_oot"]} of {A["c17_lines"]} WH03 lines outside tolerance.
  - Mis-slot at WH04: {A['misslot_sku']} short 40 in A-12-03 and over 40 in A-21-03 (nets to zero).
  - Unposted transfers: {', '.join(A['transit_skus'])} short in WH02 and over by the same quantity in WH06, with no transfer record.
  - Genuine high-value shortages at WH07 on A-class items: {', '.join(A['hv_skus'])}.

## Purchasing and payables
- Invoice register: {A['invoice_rows']} rows, total Amount {money(A['invoice_total'])}.
- POs: {A['po_rows']}. Split-PO clusters: {A['split_clusters']}, all by requester {A['split_requester']} at WH03 ({A['split_po_count']} POs, {money(A['split_total'])} in total).
- Near-duplicate invoices: {A['dup_pairs']} pairs worth {money(A['dup_value'])} (duplicate refs: {', '.join(dup_ids)}). Patterns: letter suffix, leading zeros and dashes, transposed digits, same invoice under duplicate vendor V049, same amount a few days apart.
- Invoices without a PO: {A['nopo_count']} totalling {money(A['nopo_total'])}; three are from new vendor V051 ({money(A['new_vendor_paid'])}).
- Invoice quantity above goods received: {', '.join(over_qty)}.
- Invoice price more than 2% above PO: {', '.join(over_price)}.
- Invoice dated before its PO: {', '.join(before_po)}.
- Unit-of-measure receipt: {A['uom_po']} ordered 10 CS, receipted as 120 EA.

## Vendor master
- Records: {A['vendor_rows']}. Duplicate pairs: V009/V049 (same tax ID and bank), V022/V050 (same name once standardised, same tax ID), V015/V044 (same bank and phone).
- Missing tax ID: {A['vendor_missing_tax']}. Dormant (no transaction for 18 months to 31 Oct 2026): {A['vendor_dormant']}.
- New vendor V051: created 22 Sep 2026, PO Box address, no tax ID, {money(A['new_vendor_paid'])} invoiced without POs.

## Transfers, stock health, suppliers, spend
- Transfers not received after 14+ days: {A['transfers_unreceived_14d']} ({', '.join(unrec)}). Received short: {A['transfers_short']}.
- Stock on hand {money(A['soh_value'])}; no movement for over 365 days: {A['aged365_lines']} lines worth {money(A['aged365_value'])}, most in {A['aged365_top_wh']}. Lines with more than 12 months of supply: {A['excess_lines']}.
- OTIF (on time, in full, right unit) overall {A['otif_overall']}%; worst supplier {A['otif_worst']} at {A['otif_worst_pct']}%.
- Indirect spend {money(A['spend_total'])} across {A['spend_lines']} lines; largest category {A['spend_top_cat']}; coded to 6999 Sundry: {money(A['spend_sundry'])}.
- Spend by category: {'; '.join(f"{k} {money(v)}" for k, v in A['spend_by_cat'].items())}.
"""
(OUT / "ANSWER_KEY.md").write_text(key)
with zipfile.ZipFile(OUT / "practice_pack.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for name in list(FILES) + ["README.txt", "practice_pack.xlsx"]:
        z.write(OUT / name, name)
print(json.dumps({k: A[k] for k in ["count_rows","oot_lines","network_ira","ira","lowest_wh","uom_lines","uom_wh","gross_total","split_clusters","split_po_count","dup_pairs","nopo_count","nopo_total","vendor_missing_tax","vendor_dormant","transfers_unreceived_14d","aged365_value","aged365_top_wh","excess_lines","otif_worst","otif_worst_pct","spend_top_cat","spend_sundry"]}, indent=1))
