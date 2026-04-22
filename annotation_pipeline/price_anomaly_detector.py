"""
Vlens-Trust: Price Anomaly Detection Pipeline
Dual-method detection: Z-score AND IQR must both flag an observation.
Implements Section 4.3 of the Vlens-Trust paper.
"""
import numpy as np
from typing import List, Tuple


def detect_price_anomalies(
    prices: List[float],
    z_threshold: float = 2.5,
    iqr_multiplier: float = 1.5,
) -> Tuple[List[int], List[float], dict]:
    """
    Apply dual-method anomaly detection to a product price series.

    Method 1 (Z-score): flag if |z| > z_threshold (default 2.5)
    Method 2 (IQR): flag if price < Q1 - k*IQR or price > Q3 + k*IQR
    Final label: 1 only if BOTH methods agree.

    Parameters
    ----------
    prices : List[float]
        Ordered list of price observations for one product.
    z_threshold : float
        Z-score threshold (default 2.5, as per paper Section 4.3).
    iqr_multiplier : float
        IQR multiplier k (default 1.5, standard Tukey fences).

    Returns
    -------
    anomaly_labels : List[int]
        Binary labels per observation (1 = anomaly, 0 = normal).
    z_scores : List[float]
        Z-scores for each observation.
    stats : dict
        Descriptive statistics used for detection.
    """
    if len(prices) < 7:
        raise ValueError("Price series must have at least 7 observations for valid anomaly labeling.")

    arr = np.array(prices, dtype=float)
    mean = arr.mean()
    std  = arr.std()

    if std < 1e-9:
        # Perfectly constant price series — no anomalies
        return [0] * len(prices), [0.0] * len(prices), {
            "mean": mean, "std": std, "q1": mean, "q3": mean,
            "iqr": 0, "lower_fence": mean, "upper_fence": mean
        }

    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1

    lower_fence = q1 - iqr_multiplier * iqr
    upper_fence = q3 + iqr_multiplier * iqr

    anomaly_labels = []
    z_scores = []

    for price in prices:
        z = (price - mean) / std
        z_flag  = abs(z) > z_threshold
        iqr_flag = (price < lower_fence) or (price > upper_fence)
        label = 1 if (z_flag and iqr_flag) else 0
        anomaly_labels.append(label)
        z_scores.append(round(z, 4))

    stats = {
        "n_observations":   len(prices),
        "mean":             round(mean, 2),
        "std":              round(std, 2),
        "q1":               round(q1, 2),
        "q3":               round(q3, 2),
        "iqr":              round(iqr, 2),
        "lower_fence":      round(lower_fence, 2),
        "upper_fence":      round(upper_fence, 2),
        "n_anomalies":      sum(anomaly_labels),
        "anomaly_rate":     round(sum(anomaly_labels) / len(prices), 4),
    }
    return anomaly_labels, z_scores, stats


def summarize_anomalies(prices: List[float], dates: List[str] = None) -> dict:
    """
    Summarize anomaly detection results for a single product's price series.
    """
    labels, z_scores, stats = detect_price_anomalies(prices)
    anomaly_indices = [i for i, l in enumerate(labels) if l == 1]

    summary = {**stats, "anomaly_day_indices": anomaly_indices}
    if dates:
        summary["anomaly_dates"] = [dates[i] for i in anomaly_indices]
    return summary


if __name__ == "__main__":
    # Example: Supplement product with price spikes (counterfeit inflation)
    import random
    random.seed(42)

    base_price = 999.0  # HealthKart Vitamin C 1000mg
    # Stable 25-day series
    normal_days = [base_price * (1 + random.uniform(-0.02, 0.02)) for _ in range(25)]
    # 2 injected anomalies
    anomaly_days = [base_price * 7.2, base_price * 0.04]
    prices = normal_days[:10] + anomaly_days[:1] + normal_days[10:20] + anomaly_days[1:] + normal_days[20:]

    labels, z_scores, stats = detect_price_anomalies(prices)
    print("Price Anomaly Detection — Example Output")
    print("=" * 50)
    print(f"Observations   : {stats['n_observations']}")
    print(f"Mean price     : ₹{stats['mean']:.2f}")
    print(f"Std deviation  : ₹{stats['std']:.2f}")
    print(f"IQR fences     : [₹{stats['lower_fence']:.2f}, ₹{stats['upper_fence']:.2f}]")
    print(f"Anomalies found: {stats['n_anomalies']} ({stats['anomaly_rate']*100:.1f}%)")
    print()
    for i, (p, l, z) in enumerate(zip(prices, labels, z_scores)):
        flag = " ← ANOMALY (both Z & IQR)" if l else ""
        print(f"Day {i+1:2d}: ₹{p:>10.2f}   z={z:>7.3f}{flag}")
