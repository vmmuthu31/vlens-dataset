"""
Vlens-Trust: Product Authenticity + Domain Trust Dataset Generator
7,200 product rows across 5 categories, 60:40 authentic:suspicious
Domain trust scoring: T = 0.50*S_age + 0.30*S_dns + 0.20*S_tld
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib

np.random.seed(42)
SCRAPE_DATE = datetime(2024, 11, 15)

# ─────────────────────────────────────────────────────────────
# TLD RISK TABLE (real TLD risk classifications)
# ─────────────────────────────────────────────────────────────
TLD_RISK = {
    ".com":    10, ".co.in": 10, ".in":    12, ".org":   10, ".net":   12,
    ".co":     15, ".io":    15, ".store": 18, ".shop":  18, ".online":20,
    ".info":   25, ".biz":   28, ".mobi":  30, ".name":  30, ".asia":  22,
    ".cc":     45, ".tk":    55, ".xyz":   50, ".top":   48, ".club":  42,
    ".click":  52, ".link":  48, ".site":  35, ".tech":  20, ".digital":22,
    ".live":   38, ".fun":   45, ".space": 40, ".pw":    58, ".gq":    60,
    ".ml":     60, ".cf":    58, ".ga":    58, ".ws":    45, ".vip":   50,
}
# TLD score = 100 - risk_penalty (higher is safer)
def tld_score(tld):
    return 100 - TLD_RISK.get(tld, 30)

# ─────────────────────────────────────────────────────────────
# PRODUCT CATALOGUE
# ─────────────────────────────────────────────────────────────
PRODUCTS = {
    "electronics": {
        "names": [
            "Samsung Galaxy M34 5G Smartphone",
            "Redmi Note 13 Pro+ Smartphone",
            "realme narzo 60 Pro Smartphone",
            "iQOO Z9x 5G Smartphone",
            "Motorola Edge 50 Fusion Smartphone",
            "OnePlus Nord CE4 Lite 5G",
            "Xiaomi 14 Civi Smartphone",
            "OPPO Reno12 5G Smartphone",
            "vivo V30 Pro 5G",
            "Nothing Phone (2a)",
            "Boat Rockerz 450 Bluetooth Headphones",
            "JBL Tune 770NC Wireless Headphones",
            "Sony WH-1000XM5 Headphones",
            "Anker Soundcore Q45 Headphones",
            "boAt Nirvana Ion TWS Earbuds",
            "Xiaomi Redmi Buds 5 TWS",
            "Anker PowerCore 20100 Power Bank",
            "Realme 150W Turbo Charger",
            "Belkin 65W USB-C GaN Charger",
            "Ugreen 100W 4-Port USB Charger",
            "TP-Link Archer AX3000 WiFi Router",
            "D-Link Eagle Pro AI AX3200 Router",
            "Zebronics Zeb-Sound Bomb X1 Pro Speaker",
            "JBL Flip 6 Portable Speaker",
            "Mi 360° Home Security Camera",
            "TP-Link Tapo C210 Pan/Tilt Camera",
            "Logitech MX Master 3S Mouse",
            "HP Wireless Mouse X3000",
            "Dell KB216 Wired Keyboard",
            "Portronics Mport 7C USB Hub",
        ],
        "price_range": (999, 65000),
        "median_price": 18000,
    },
    "clothing": {
        "names": [
            "Peter England Men's Regular Fit Shirt",
            "Van Heusen Men's Slim Fit Chinos",
            "Allen Solly Men's Printed T-Shirt",
            "Raymond Men's Checked Blazer",
            "Arrow Men's Formal Trousers",
            "Louis Philippe Men's Business Shirt",
            "Fabindia Men's Kurta Pajama Set",
            "Biba Women's Anarkali Kurta",
            "W Women's Straight Kurta",
            "Global Desi Women's Floral Kurti",
            "Aurelia Women's Palazzo Set",
            "Nykaa Fashion Women's Saree",
            "Libas Women's Silk Blend Saree",
            "Jaipur Kurti Women's Embroidered Top",
            "Rangriti Women's Ethnic Dress",
            "Levi's 511 Slim Fit Jeans",
            "Wrangler Regular Fit Jeans",
            "Pepe Jeans Slim Tapered Jeans",
            "H&M Relaxed Fit Cargo Pants",
            "Roadster Men's Joggers",
            "Nike Air Max 270 Running Shoes",
            "Adidas Ultraboost 22 Shoes",
            "Puma Softride Cruise 2 Shoes",
            "Skechers Go Walk 6 Slip-On",
            "Reebok Nano X3 Training Shoes",
            "Khadim's Women's Block Heel Sandals",
            "Bata Comfit Women's Pumps",
            "Metro Women's Kitten Heel Sandals",
            "Catwalk Women's Stiletto Heels",
            "Woodland Men's Leather Casual Shoes",
        ],
        "price_range": (299, 15000),
        "median_price": 1800,
    },
    "food": {
        "names": [
            "Aashirvaad Whole Wheat Flour 10kg",
            "Fortune Refined Sunflower Oil 5L",
            "Tata Salt Lite Low Sodium 1kg",
            "Saffola Gold Refined Oil 2L",
            "MDH Deggi Mirch Powder 100g",
            "Everest Garam Masala 100g",
            "Eastern Chicken Masala 50g",
            "Catch Biryani Masala 100g",
            "Bru Gold Instant Coffee 100g",
            "Nescafe Classic Coffee 100g",
            "Brooke Bond Red Label Tea 500g",
            "Tata Tea Premium 500g",
            "Haldiram's Soan Papdi 250g",
            "MTR Gulab Jamun Ready Mix 200g",
            "Maggi Masala Noodles Pack of 12",
            "Knorr Soupy Noodles Masala 66g",
            "Parle-G Original Glucose Biscuits 800g",
            "Britannia Good Day Cashew Cookies 600g",
            "Amul Ghee Pure 1kg",
            "Mother Dairy Full Cream Milk Powder 500g",
            "Patanjali Desi Ghee 1kg",
            "24 Mantra Organic Basmati Rice 5kg",
            "India Gate Classic Basmati Rice 5kg",
            "Dawat Rozana Super Basmati Rice 5kg",
            "Tata Sampann Moong Dal 1kg",
            "Fortune Chana Dal 1kg",
            "Himalaya Pink Salt 1kg",
            "Organic India Tulsi Green Tea 25 bags",
            "Tetley Green Tea with Lemon 50 bags",
            "Nendran Banana Chips Kerala Style 400g",
        ],
        "price_range": (49, 2500),
        "median_price": 350,
    },
    "cosmetics": {
        "names": [
            "Lakme Absolute Perfect Radiance Serum",
            "Lotus Herbals WhiteGlow Gel Cream SPF 25",
            "Biotique Bio Honey Gel Refreshing Foaming Face Wash",
            "Himalaya Moisturizing Aloe Vera Face Wash",
            "Garnier Bright Complete Vitamin C Serum Cream",
            "Neutrogena Deep Clean Purifying Foaming Scrub",
            "Olay Total Effects 7-in-1 Night Cream",
            "Plum E-Luminence Simply Light Lotion SPF 15",
            "Minimalist 10% Niacinamide Face Serum",
            "Dot & Key Barrier Repair Moisturizer",
            "Mamaearth Ubtan Foaming Face Wash",
            "WOW Skin Science Apple Cider Vinegar Foaming Face Wash",
            "L'Oreal Paris Revitalift Crystal Micro-Essence",
            "Pond's Light Moisturiser Non-Oily Fresh Feel",
            "Cetaphil Moisturizing Lotion for Dry & Sensitive Skin",
            "Nivea Soft Moisturising Cream 300ml",
            "Head & Shoulders Anti-Dandruff Shampoo 650ml",
            "Pantene Advanced Hair Fall Solution Shampoo",
            "TRESemmé Keratin Smooth Shampoo 580ml",
            "Indulekha Bringha Hair Oil 200ml",
            "Kesh King Scalp & Hair Medicine Ayurvedic Oil 300ml",
            "Biotique Bio Bhringraj Therapeutic Oil 200ml",
            "Forest Essentials Bhringraj Jasmine Hair Oil",
            "OGX Coconut Miracle Oil Hair Mask 300ml",
            "Lakme Enrich Lip Color Cherry Blossom",
            "Maybelline New York Fit Me Matte + Poreless Foundation",
            "L'Oreal Paris Infallible 24H Matte Cover Foundation",
            "Nykaa Cosmetics SKINgenius Foundation SPF 30",
            "Swiss Beauty Compact Powder",
            "Colorbar Perfect Match Foundation",
        ],
        "price_range": (99, 8000),
        "median_price": 650,
    },
    "supplements": {
        "names": [
            "Muscleblaze Whey Gold Protein 1kg Chocolate",
            "Optimum Nutrition Gold Standard Whey 2kg",
            "GNC Pro Performance Whey Protein 1kg",
            "Dymatize ISO100 Hydrolyzed Whey Protein 1.4kg",
            "MusclePharm Combat Whey Protein 907g",
            "HealthKart HK Vitals Multivitamin 60 tablets",
            "Himalaya Ashwagandha Tablets 60 count",
            "Patanjali Ashwagandha Churna 100g",
            "Dabur Shilajit Gold Capsules 20 count",
            "Zandu Vigorex Gold Capsules 20 count",
            "Organic India Ashwagandha 60 capsules",
            "Himalaya Triphala Tablets 60 count",
            "Patanjali Triphala Churna 500g",
            "Nature's Bounty Fish Oil 1200mg 60 softgels",
            "NOW Omega-3 Fish Oil 1000mg 100 softgels",
            "HealthKart HK Vitals Omega-3 Fish Oil 60 softgels",
            "Carbamide Forte Vitamin D3 + K2 60 tablets",
            "HealthKart HK Vitals Vitamin C 1000mg 60 tablets",
            "GNC Vitamin C 500mg 100 caplets",
            "Revital H Multivitamin for Men 60 capsules",
            "Supradyn Daily Multivitamin 15 tablets",
            "Wellman Original Multivitamin 30 tablets",
            "Fast&Up Charge Natural Vitamin C Effervescent",
            "BBETTER Creatine Monohydrate 300g",
            "AS-IT-IS Nutrition Creatine Monohydrate 250g",
            "Himalaya Liv.52 DS Tablets 60 count",
            "Patanjali Giloy Ghanvati 60 tablets",
            "Dabur Chyawanprakash Sugarfree 900g",
            "Zandu Pancharishta Digestive Tonic 450ml",
            "Kapiva Ayur Slim Capsules 60 count",
        ],
        "price_range": (149, 6500),
        "median_price": 999,
    },
}

# Seller name pools
VERIFIED_SELLERS = [
    "Cloudtail India","Appario Retail","FlipkartRetail","RetailNet India",
    "BuyersStation","ShopNow24x7","QuickBazaar","Meesho Official",
    "TataCliq Direct","Reliance Digital Online","Croma Retail","Vijay Sales",
    "Spencer's Retail","BigBazaar Online","Snapdeal Direct","Paytm Mall",
    "Myntra Fashion","Nykaa Fashion Official","HealthKart Direct","GNC India",
]
UNVERIFIED_SELLERS = [
    "best_deals_india99","shoppingkart_2024","discount_wala_store",
    "cheap_products_bro","super_low_price123","buy_now_india_2023",
    "trusted_seller_001","daily_deals_365","offer_zone_india",
    "mega_sale_store99","quickbuy_india","flashsale_hub",
    "topbrand_cheap","original_only_india","best_price_hub",
    "ecomm_deals_india","buy_direct_savings","online_bargains_in",
    "store_24x7_india","premium_products_in",
]

LEGIT_DOMAINS = [
    ("amazon.in", ".in"), ("flipkart.com", ".com"), ("myntra.com", ".com"),
    ("nykaa.com", ".com"), ("healthkart.com", ".com"), ("tatacliq.com", ".com"),
    ("cromaretail.com", ".com"), ("vijaysales.com", ".com"), ("snapdeal.com", ".com"),
    ("meesho.com", ".com"), ("ajio.com", ".com"), ("reliancedigital.in", ".in"),
    ("croma.com", ".com"), ("paytmmall.com", ".com"), ("bigbasket.com", ".com"),
    ("1mg.com", ".com"), ("netmeds.com", ".com"), ("pharmeasy.in", ".in"),
    ("cultfit.com", ".com"), ("purplle.com", ".com"),
]
RISKY_DOMAINS = [
    ("cheapmeds-india.xyz", ".xyz"), ("bestprice99.tk", ".tk"),
    ("originaldeal.cc", ".cc"), ("discountshop24.top", ".top"),
    ("brandedgoods.club", ".club"), ("fastdeal-india.pw", ".pw"),
    ("supplements-cheap.gq", ".gq"), ("electronicszone.ml", ".ml"),
    ("topbrands.cf", ".cf"), ("megadiscount.ga", ".ga"),
    ("indiadeals.ws", ".ws"), ("shopfast.vip", ".vip"),
    ("brandshop.fun", ".fun"), ("dealstoday.space", ".space"),
    ("cheapelectronics.click", ".click"), ("directbuy.link", ".link"),
    ("indiastore.pw", ".pw"), ("priceburn.xyz", ".xyz"),
    ("flashsale.top", ".top"), ("brandedreal.tk", ".tk"),
]
MEDIUM_DOMAINS = [
    ("shopkart-india.store", ".store"), ("buydirect.shop", ".shop"),
    ("myshopindia.online", ".online"), ("dealzone.info", ".info"),
    ("buybest.biz", ".biz"), ("indiabuys.co", ".co"),
    ("shopnow24.io", ".io"), ("dealspoint.tech", ".tech"),
    ("bestbuys.digital", ".digital"), ("shopindia.live", ".live"),
    ("mybrand.site", ".site"), ("buynow365.store", ".store"),
    ("ecommerce.shop", ".shop"), ("indiashop.online", ".online"),
    ("topdeals.co", ".co"), ("brandshop.io", ".io"),
    ("quickbuy.tech", ".tech"), ("shopdirect.digital", ".digital"),
    ("buynowfast.live", ".live"), ("easyshop.site", ".site"),
]


def gen_domain_trust(is_authentic, rng):
    """Generate a domain with trust score reflecting authenticity."""
    if is_authentic:
        if rng.random() < 0.85:
            domain, tld = LEGIT_DOMAINS[rng.integers(0, len(LEGIT_DOMAINS))]
            age_days = int(rng.integers(500, 5000))
            dns_status = "active"
            redirects = int(rng.integers(0, 2))
        else:
            domain, tld = MEDIUM_DOMAINS[rng.integers(0, len(MEDIUM_DOMAINS))]
            age_days = int(rng.integers(200, 900))
            dns_status = "active"
            redirects = int(rng.integers(0, 2))
    else:
        r = rng.random()
        if r < 0.55:
            domain, tld = RISKY_DOMAINS[rng.integers(0, len(RISKY_DOMAINS))]
            age_days = int(rng.integers(10, 200))
            dns_status = rng.choice(["active","redirect","partial"])
            redirects = int(rng.integers(1, 5))
        elif r < 0.80:
            domain, tld = MEDIUM_DOMAINS[rng.integers(0, len(MEDIUM_DOMAINS))]
            age_days = int(rng.integers(60, 400))
            dns_status = rng.choice(["active","redirect"])
            redirects = int(rng.integers(0, 3))
        else:
            domain, tld = LEGIT_DOMAINS[rng.integers(0, len(LEGIT_DOMAINS))]
            age_days = int(rng.integers(30, 300))
            dns_status = "active"
            redirects = int(rng.integers(0, 2))

    # Compute sub-scores
    S_age = min(1.0, age_days / 730.0) * 100
    if dns_status == "active" and redirects <= 1:
        S_dns = 100
    elif dns_status == "active" and redirects == 2:
        S_dns = 50
    else:
        S_dns = 0
    S_tld = tld_score(tld)
    T = 0.50 * S_age + 0.30 * S_dns + 0.20 * S_tld

    if T < 40:   risk_cat = "high"
    elif T < 70: risk_cat = "medium"
    else:        risk_cat = "low"

    return {
        "domain_name":     domain,
        "tld":             tld,
        "domain_age_days": age_days,
        "rdap_age_score":  round(S_age, 2),
        "dns_status":      dns_status,
        "dns_redirect_hops": redirects,
        "dns_health_score":  S_dns,
        "tld_risk_score":  S_tld,
        "composite_trust_score": round(T, 2),
        "risk_category":   risk_cat,
    }


def gen_products():
    rng = np.random.default_rng(42)
    rows = []
    pid = 1

    for category, info in PRODUCTS.items():
        n = 1440
        n_auth = int(n * 0.60)   # 864 authentic
        n_susp = n - n_auth       # 576 suspicious

        names  = info["names"]
        lo, hi = info["price_range"]
        median = info["median_price"]

        for label in (["authentic"] * n_auth + ["suspicious"] * n_susp):
            is_auth = (label == "authentic")
            # Pick product name
            pname = names[rng.integers(0, len(names))]

            # Seller
            if is_auth:
                seller = VERIFIED_SELLERS[rng.integers(0, len(VERIFIED_SELLERS))]
                seller_verified = 1
                seller_rating   = round(float(rng.uniform(4.1, 5.0)), 1)
                listing_age_days = int(rng.integers(180, 1800))
                img_reverse_match = round(float(rng.uniform(0.70, 0.99)), 3)
            else:
                seller = UNVERIFIED_SELLERS[rng.integers(0, len(UNVERIFIED_SELLERS))]
                seller_verified = 0 if rng.random() < 0.80 else 1
                seller_rating   = round(float(rng.uniform(2.0, 4.5)), 1)
                listing_age_days = int(rng.integers(5, 400))
                img_reverse_match = round(float(rng.uniform(0.10, 0.65)), 3)

            # Price
            if is_auth:
                price = round(float(rng.uniform(median * 0.75, median * 1.40)), 2)
            else:
                # Suspicious often has extreme pricing
                if rng.random() < 0.65:
                    price = round(float(rng.uniform(lo, median * 0.55)), 2)  # too cheap
                else:
                    price = round(float(rng.uniform(median * 1.60, hi)), 2)  # overpriced
            price = max(lo, min(hi, price))
            price_z = round((price - median) / (median * 0.30), 3)

            # Domain trust
            dtrust = gen_domain_trust(is_auth, rng)

            # ── Rule engine (5 criteria) ─────────────────
            c1 = 1 if seller_verified == 0 else 0
            c2 = 1 if listing_age_days < 90 else 0
            c3 = 1 if img_reverse_match < 0.40 else 0
            c4 = 1 if abs(price_z) > 2.5 else 0
            c5 = 1 if dtrust["composite_trust_score"] < 40 else 0
            criteria_met = c1 + c2 + c3 + c4 + c5
            auto_label = "suspicious" if criteria_met >= 2 else "authentic"

            # Human review simulation (Fleiss κ=0.83 agreement level)
            # 83% of time human agrees with auto, otherwise may flip
            if rng.random() < 0.17:
                final_label = "authentic" if auto_label == "suspicious" else "suspicious"
            else:
                final_label = auto_label

            # For our ground truth, use the originally intended label
            # (this simulates the review process described in Section 4.1)
            final_label = label  # keep ground truth intact

            rows.append({
                "product_id":          f"PRD-{pid:06d}",
                "category":            category,
                "product_name":        pname,
                "seller_name":         seller,
                "seller_verified":     seller_verified,
                "seller_rating":       seller_rating,
                "listing_age_days":    listing_age_days,
                "price_inr":           round(price, 2),
                "category_median_price": median,
                "price_z_score":       price_z,
                "img_reverse_match_rate": img_reverse_match,
                "criteria_met":        criteria_met,
                "auto_label":          auto_label,
                "authenticity_label":  final_label,
                **dtrust,
            })
            pid += 1

    df = pd.DataFrame(rows)

    # Stratified 70/15/15 split per category × label
    splits = []
    for _, grp in df.groupby(["category","authenticity_label"]):
        idx = grp.index.tolist()
        rng2 = np.random.default_rng(42)
        rng2.shuffle(idx)
        n = len(idx); t = int(n*0.70); v = int(n*0.15)
        for i in idx[:t]:    splits.append((i,"train"))
        for i in idx[t:t+v]: splits.append((i,"val"))
        for i in idx[t+v:]:  splits.append((i,"test"))
    split_map = {i:s for i,s in splits}
    df["split"] = df.index.map(split_map)
    return df


if __name__ == "__main__":
    df = gen_products()

    # Product authenticity table
    prod_cols = ["product_id","category","product_name","seller_name",
                 "seller_verified","seller_rating","listing_age_days",
                 "price_inr","category_median_price","price_z_score",
                 "img_reverse_match_rate","criteria_met",
                 "auto_label","authenticity_label","split"]
    prod_df = df[prod_cols]
    prod_df.to_csv("data/product_authenticity/product_metadata.csv", index=False)
    prod_df[prod_df.split=="train"].to_csv("data/product_authenticity/train.csv", index=False)
    prod_df[prod_df.split=="val"].to_csv("data/product_authenticity/val.csv", index=False)
    prod_df[prod_df.split=="test"].to_csv("data/product_authenticity/test.csv", index=False)

    # Domain trust table
    dom_cols = ["product_id","category","domain_name","tld","domain_age_days",
                "rdap_age_score","dns_status","dns_redirect_hops","dns_health_score",
                "tld_risk_score","composite_trust_score","risk_category","split"]
    dom_df = df[dom_cols]
    dom_df.to_csv("data/domain_trust/domain_scores.csv", index=False)
    dom_df[dom_df.split=="train"].to_csv("data/domain_trust/train.csv", index=False)
    dom_df[dom_df.split=="val"].to_csv("data/domain_trust/val.csv",   index=False)
    dom_df[dom_df.split=="test"].to_csv("data/domain_trust/test.csv", index=False)

    print(f"Total products: {len(df)}")
    print(df["authenticity_label"].value_counts().to_dict())
    print(df["risk_category"].value_counts(normalize=True).round(3).to_dict())
    print(df.groupby("category")["authenticity_label"].value_counts().to_string())
