"""
Vlens-Trust: Domain Trust Scoring Pipeline
Implements the RDAP + DNS + TLD rule engine described in Section 4.4
Composite trust score: T = 0.50*S_age + 0.30*S_dns + 0.20*S_tld
"""

# TLD risk penalty table (higher penalty = less trustworthy TLD)
TLD_RISK_PENALTIES = {
    # Baseline trusted TLDs
    ".com":    10, ".co.in": 10, ".in":    12, ".org":   10, ".net":   12,
    ".co":     15, ".io":    15, ".store": 18, ".shop":  18, ".online": 20,
    ".info":   25, ".biz":   28, ".mobi":  30, ".name":  30, ".asia":  22,
    # Medium risk
    ".tech":   20, ".digital": 22, ".site": 35, ".live":  38, ".space": 40,
    ".club":   42, ".link":   48, ".click": 52,
    # High risk (historically associated with spam/fraud)
    ".cc":     45, ".tk":    55, ".xyz":   50, ".top":   48,
    ".vip":    50, ".fun":   45, ".pw":    58, ".gq":    60,
    ".ml":     60, ".cf":    58, ".ga":    58, ".ws":    45,
}


def compute_rdap_age_score(domain_age_days: int) -> float:
    """
    RDAP age score: full score at 2 years (730 days).
    S_age = min(1, domain_age_days / 730) * 100
    Domains registered < 180 days are high-risk.
    """
    return min(1.0, domain_age_days / 730.0) * 100.0


def compute_dns_health_score(dns_status: str, redirect_hops: int) -> float:
    """
    DNS health score based on resolution status and redirect chain length.
    - Active DNS, ≤1 redirect hop: 100 (healthy)
    - Active DNS, 2 redirect hops: 50 (caution)
    - Partial resolution or >2 hops: 0 (high-risk)
    """
    if dns_status == "active" and redirect_hops <= 1:
        return 100.0
    elif dns_status == "active" and redirect_hops == 2:
        return 50.0
    else:
        return 0.0


def compute_tld_risk_score(tld: str) -> float:
    """
    TLD risk score from curated table.
    S_tld = 100 - risk_penalty
    Unknown TLDs default to penalty of 30 (moderate risk).
    """
    penalty = TLD_RISK_PENALTIES.get(tld.lower(), 30)
    return float(100 - penalty)


def compute_composite_trust_score(
    domain_age_days: int,
    dns_status: str,
    redirect_hops: int,
    tld: str,
    weight_age: float = 0.50,
    weight_dns: float = 0.30,
    weight_tld: float = 0.20,
) -> dict:
    """
    Compute the composite domain trust score for a seller domain.

    Parameters
    ----------
    domain_age_days : int
        Days since domain registration (from RDAP query).
    dns_status : str
        DNS resolution status: 'active', 'redirect', or 'partial'.
    redirect_hops : int
        Number of DNS redirect hops detected.
    tld : str
        Top-level domain string (e.g., '.com', '.xyz').
    weight_age, weight_dns, weight_tld : float
        Weights for the three sub-scores (must sum to 1.0).

    Returns
    -------
    dict with all sub-scores, composite score, and risk category.
    """
    S_age = compute_rdap_age_score(domain_age_days)
    S_dns = compute_dns_health_score(dns_status, redirect_hops)
    S_tld = compute_tld_risk_score(tld)

    T = weight_age * S_age + weight_dns * S_dns + weight_tld * S_tld

    if T < 40:
        risk_category = "high"
    elif T < 70:
        risk_category = "medium"
    else:
        risk_category = "low"

    return {
        "rdap_age_score":      round(S_age, 2),
        "dns_health_score":    round(S_dns, 2),
        "tld_risk_score":      round(S_tld, 2),
        "composite_trust_score": round(T, 2),
        "risk_category":       risk_category,
        "is_high_risk":        risk_category == "high",
    }


if __name__ == "__main__":
    # Example usage
    examples = [
        {"domain": "flipkart.com",       "age_days": 5840, "dns": "active",   "hops": 0,  "tld": ".com"},
        {"domain": "dealzone.info",      "age_days": 200,  "dns": "active",   "hops": 2,  "tld": ".info"},
        {"domain": "cheapmeds.xyz",      "age_days": 45,   "dns": "partial",  "hops": 3,  "tld": ".xyz"},
        {"domain": "shopkart.store",     "age_days": 280,  "dns": "active",   "hops": 1,  "tld": ".store"},
        {"domain": "bestprice99.tk",     "age_days": 30,   "dns": "redirect", "hops": 4,  "tld": ".tk"},
    ]
    print(f"{'Domain':<30} {'Score':>6} {'Risk':<8} {'S_age':>6} {'S_dns':>6} {'S_tld':>6}")
    print("-" * 70)
    for e in examples:
        result = compute_composite_trust_score(e["age_days"], e["dns"], e["hops"], e["tld"])
        print(f"{e['domain']:<30} {result['composite_trust_score']:>6.1f} "
              f"{result['risk_category']:<8} {result['rdap_age_score']:>6.1f} "
              f"{result['dns_health_score']:>6.1f} {result['tld_risk_score']:>6.1f}")
