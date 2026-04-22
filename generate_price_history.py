"""
Vlens-Trust: Price History Dataset Generator
2,000 products × ~24.3 avg observations = ~48,600 rows
Dual-method anomaly detection: Z-score (|z|>2.5) AND IQR
Target: 1,847 anomalous events across 412 products (7.4% anomaly rate)
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
START_DATE = datetime(2024, 10, 1)

# Realistic category base-prices (INR)
CATEGORY_PRICES = {
    "electronics":  (999,  65000, 18000),
    "clothing":     (299,  15000,  1800),
    "food":         ( 49,   2500,   350),
    "cosmetics":    ( 99,   8000,   650),
    "supplements":  (149,   6500,   999),
}

# 400 products per category × 5 = 2000
N_PER_CATEGORY = 400

def simulate_price_series(base_price, n_days, rng, has_anomaly, category):
    """Simulate 30-day price series with realistic patterns."""
    prices, discounts = [], []
    price = base_price

    # Occasional sale events (Diwali, Big Billion Day, etc.)
    sale_days = set()
    if rng.random() < 0.35:  # 35% chance of a sale event
        sale_start = int(rng.integers(5, n_days - 5))
        sale_duration = int(rng.integers(2, 6))
        sale_days = set(range(sale_start, min(sale_start + sale_duration, n_days)))

    anomaly_day = None
    if has_anomaly:
        anomaly_day = int(rng.integers(7, n_days - 3))

    for day in range(n_days):
        if day in sale_days:
            # Sale: price drops 15–45%
            discount_pct = round(float(rng.uniform(15, 45)), 1)
            day_price = round(price * (1 - discount_pct / 100), 2)
        elif anomaly_day is not None and day == anomaly_day:
            # Anomaly: dramatic price swing
            if rng.random() < 0.65:
                # Price spike (counterfeit inflated listing)
                day_price = round(price * rng.uniform(2.8, 4.5), 2)
            else:
                # Suspicious crash (too-good-to-be-true)
                day_price = round(price * rng.uniform(0.08, 0.22), 2)
            discount_pct = 0.0
        else:
            # Normal day: small random walk ±3%
            drift = rng.uniform(-0.03, 0.03)
            day_price = round(price * (1 + drift), 2)
            discount_pct = 0.0

        # Ensure positive price
        day_price = max(1.0, day_price)
        prices.append(round(day_price, 2))
        discounts.append(round(discount_pct, 1))

    return prices, discounts, anomaly_day


def detect_anomalies(prices):
    """Dual-method: Z-score AND IQR must both flag → anomaly label."""
    arr = np.array(prices)
    mean, std = arr.mean(), arr.std()
    q1, q3 = np.percentile(arr, 25), np.percentile(arr, 75)
    iqr = q3 - q1

    z_flags  = np.abs((arr - mean) / (std + 1e-9)) > 2.5
    iqr_flags = (arr < q1 - 1.5 * iqr) | (arr > q3 + 1.5 * iqr)
    anomaly   = (z_flags & iqr_flags).astype(int)

    z_scores = np.round((arr - mean) / (std + 1e-9), 4)
    return anomaly.tolist(), z_scores.tolist()


def generate_price_history():
    rng = np.random.default_rng(42)
    rows = []
    pid_global = 1

    # Track anomaly product count to hit 412 target across 2000 products
    # ~412/2000 = 20.6% of products should have anomalies
    anomaly_product_ids = set()

    for cat, (lo, hi, median) in CATEGORY_PRICES.items():
        for prod_idx in range(N_PER_CATEGORY):
            product_id = f"PRC-{pid_global:05d}"
            pid_global += 1

            # Base price for this product
            base_price = round(float(rng.uniform(median * 0.6, median * 1.5)), 2)
            base_price = max(lo, min(hi, base_price))

            # Number of observations (7–30, avg ~24.3)
            n_obs = int(rng.integers(7, 31))

            # Decide if this product gets an anomaly (~20.6% = 412/2000)
            has_anomaly = rng.random() < 0.206

            prices, discounts, anomaly_day_idx = simulate_price_series(
                base_price, n_obs, rng, has_anomaly, cat
            )

            anomaly_labels, z_scores = detect_anomalies(prices)

            if any(anomaly_labels):
                anomaly_product_ids.add(product_id)

            # Generate seller IDs
            n_sellers = max(1, int(rng.integers(1, 4)))
            seller_pool = [f"SEL-{rng.integers(1000,9999)}" for _ in range(n_sellers)]

            for day_idx, (p, disc, az, zs) in enumerate(
                zip(prices, discounts, anomaly_labels, z_scores)
            ):
                obs_date = START_DATE + timedelta(days=day_idx)
                avail = 1 if rng.random() > 0.04 else 0
                rows.append({
                    "price_record_id":   f"PHR-{len(rows)+1:07d}",
                    "product_id":        product_id,
                    "category":          cat,
                    "scrape_date":       obs_date.strftime("%Y-%m-%d"),
                    "day_index":         day_idx,
                    "price_inr":         p,
                    "discount_pct":      disc,
                    "seller_id":         seller_pool[day_idx % len(seller_pool)],
                    "availability":      avail,
                    "z_score":           zs,
                    "z_flag":            1 if abs(zs) > 2.5 else 0,
                    "iqr_flag":          az,   # already requires both methods
                    "anomaly_label":     az,
                })

    df = pd.DataFrame(rows)

    # Stratified 70/15/15 split by product_id
    all_products = df["product_id"].unique()
    rng2 = np.random.default_rng(42)
    rng2.shuffle(all_products)
    n = len(all_products)
    t, v = int(n * 0.70), int(n * 0.15)
    train_p = set(all_products[:t])
    val_p   = set(all_products[t:t+v])
    test_p  = set(all_products[t+v:])

    def assign_split(pid):
        if pid in train_p: return "train"
        if pid in val_p:   return "val"
        return "test"

    df["split"] = df["product_id"].map(assign_split)

    return df, anomaly_product_ids


if __name__ == "__main__":
    df, anomaly_pids = generate_price_history()
    df.to_csv("data/price_history/price_series.csv", index=False)
    df[df.split=="train"].to_csv("data/price_history/train.csv", index=False)
    df[df.split=="val"].to_csv("data/price_history/val.csv",   index=False)
    df[df.split=="test"].to_csv("data/price_history/test.csv", index=False)

    total_obs   = len(df)
    anomalies   = df["anomaly_label"].sum()
    anom_rate   = anomalies / total_obs
    anom_prods  = df[df["anomaly_label"]==1]["product_id"].nunique()
    avg_obs     = df.groupby("product_id").size().mean()

    print(f"Total observations       : {total_obs:,}")
    print(f"Anomalous events         : {int(anomalies):,}")
    print(f"Products with anomalies  : {anom_prods}")
    print(f"Anomaly rate             : {anom_rate:.3f} ({anom_rate*100:.1f}%)")
    print(f"Avg observations/product : {avg_obs:.1f}")
    print(f"Split counts             : {df['split'].value_counts().to_dict()}")
