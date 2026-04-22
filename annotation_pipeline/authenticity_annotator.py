"""
Vlens-Trust: Product Authenticity Annotation Pipeline
5-criterion rule engine + majority-vote human verification
Implements Section 4.1 of the Vlens-Trust paper.
"""


def evaluate_five_criteria(
    seller_verified: int,
    listing_age_days: int,
    img_reverse_match_rate: float,
    price_z_score: float,
    composite_trust_score: float,
    age_threshold: int = 90,
    match_rate_threshold: float = 0.40,
    price_z_threshold: float = 2.5,
    trust_score_threshold: float = 40.0,
) -> dict:
    """
    Evaluate the 5-criterion rule engine for product authenticity.

    A product is automatically labeled 'suspicious' if 2+ criteria are met.
    Borderline cases (exactly 2 criteria) are escalated for human review.

    Criteria
    --------
    C1: Seller not platform-verified
    C2: Listing age < 90 days
    C3: Image reverse-search match rate < 0.40
    C4: Price deviation |z| > 2.5 from category median
    C5: Domain composite trust score < 40

    Returns
    -------
    dict with individual criterion flags, total count, and preliminary label.
    """
    c1 = 1 if seller_verified == 0 else 0
    c2 = 1 if listing_age_days < age_threshold else 0
    c3 = 1 if img_reverse_match_rate < match_rate_threshold else 0
    c4 = 1 if abs(price_z_score) > price_z_threshold else 0
    c5 = 1 if composite_trust_score < trust_score_threshold else 0

    criteria_met = c1 + c2 + c3 + c4 + c5
    auto_label = "suspicious" if criteria_met >= 2 else "authentic"
    needs_review = criteria_met == 2  # Borderline case

    return {
        "c1_unverified_seller":   c1,
        "c2_young_listing":       c2,
        "c3_image_mismatch":      c3,
        "c4_price_anomaly":       c4,
        "c5_low_trust_score":     c5,
        "criteria_met":           criteria_met,
        "auto_label":             auto_label,
        "needs_human_review":     needs_review,
        "escalation_reason":      "Borderline: exactly 2 criteria met" if needs_review else None,
    }


def majority_vote(annotator_labels: list) -> str:
    """
    Resolve disagreements among multiple annotators by majority vote.
    Expects a list of 'authentic' or 'suspicious' strings.
    Raises ValueError if no majority (even number with equal split).
    """
    if not annotator_labels:
        raise ValueError("No annotator labels provided.")
    suspicious_count = sum(1 for l in annotator_labels if l == "suspicious")
    authentic_count  = len(annotator_labels) - suspicious_count
    if suspicious_count > authentic_count:
        return "suspicious"
    elif authentic_count > suspicious_count:
        return "authentic"
    else:
        raise ValueError(f"Tie in {len(annotator_labels)}-annotator vote. Manual adjudication required.")


if __name__ == "__main__":
    print("5-Criterion Rule Engine — Example Evaluations")
    print("=" * 65)
    cases = [
        {"name": "Flipkart verified seller, old listing, normal price",
         "seller_verified":1, "listing_age_days":540, "img_reverse_match_rate":0.92,
         "price_z_score":0.3, "composite_trust_score":88.5},
        {"name": "Unverified seller, young listing, suspicious price",
         "seller_verified":0, "listing_age_days":45, "img_reverse_match_rate":0.28,
         "price_z_score":3.8, "composite_trust_score":12.1},
        {"name": "Borderline case (exactly 2 criteria)",
         "seller_verified":0, "listing_age_days":60, "img_reverse_match_rate":0.75,
         "price_z_score":1.2, "composite_trust_score":65.0},
    ]
    for case in cases:
        name = case.pop("name")
        result = evaluate_five_criteria(**case)
        print(f"\n{name}")
        print(f"  Criteria met: {result['criteria_met']}/5  → {result['auto_label'].upper()}"
              f"  {'[NEEDS REVIEW]' if result['needs_human_review'] else ''}")
        flags = [k for k,v in result.items() if k.startswith("c") and v==1]
        if flags: print(f"  Triggered: {', '.join(flags)}")
