# Vlens-Trust: A Multimodal Dataset for Product Authenticity and Visual Intelligence

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Dataset Size](https://img.shields.io/badge/Dataset-12%2C400%20samples-blue)](https://github.com/vmmuthu31/vlens-dataset)
[![Paper](https://img.shields.io/badge/Paper-MTAP%202026-green)](https://github.com/vmmuthu31/vlens-dataset)

> **Vlens-Trust** is the first publicly available multimodal dataset unifying four complementary data dimensions: product image-based authenticity labels, biological species annotations, scraped price histories with anomaly flags, and domain-level trust scores — designed for integrated e-commerce fraud detection research.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Statistics](#dataset-statistics)
- [Data Modalities](#data-modalities)
- [Repository Structure](#repository-structure)
- [Usage](#usage)
- [Benchmark Results](#benchmark-results)
- [Data Format](#data-format)
- [Annotation Methodology](#annotation-methodology)
- [Citation](#citation)
- [License](#license)

---

## Overview

The proliferation of counterfeit products and fraudulent online listings is a critical challenge for e-commerce platforms worldwide. Existing datasets address product authenticity, species recognition, or pricing anomalies *in isolation* — leaving a significant gap for integrated multimodal analysis.

**Vlens-Trust bridges this gap** by providing:

1. **Product authenticity labels** (authentic / suspicious) for 7,200 product images across 5 categories collected from Indian e-commerce platforms.
2. **Biological species annotations** with real taxonomy (genus, family, scientific name) for 3,200 plant and animal species relevant to supplement and cosmetic labeling.
3. **Price anomaly flags** across 2,000 30-day product price series, with dual-method Z-score + IQR anomaly detection.
4. **Domain trust scores** (0–100 continuous scale) derived from RDAP age, DNS health, and TLD risk analysis for each seller domain.

---

## Dataset Statistics

| Modality | Component | Total | Train (70%) | Val (15%) | Test (15%) |
|---|---|---|---|---|---|
| Product Authenticity | Electronics | 1,440 | 1,008 | 216 | 216 |
| | Clothing | 1,440 | 1,008 | 216 | 216 |
| | Food | 1,440 | 1,008 | 216 | 216 |
| | Cosmetics | 1,440 | 1,008 | 216 | 216 |
| | Supplements | 1,440 | 1,008 | 216 | 216 |
| Species | Plant Species | 1,600 | 1,120 | 240 | 240 |
| | Animal Species | 1,600 | 1,120 | 240 | 240 |
| Price History | Product Price Series | 2,000 | 1,400 | 300 | 300 |
| **TOTAL** | | **12,400** | **8,680** | **1,860** | **1,860** |

### Key Statistics

| Metric | Value |
|---|---|
| Total annotated samples | 12,400 |
| Total price observations | ~49,000 |
| Authentic : Suspicious ratio (T1) | 60 : 40 |
| High-risk : Medium-risk : Low-risk domains (T3) | 23.1% : 41.7% : 35.2% |
| Anomalous price events (T4) | 1,853 across 412 products |
| Inter-annotator agreement (Fleiss' κ) | 0.83 |
| Domain trust validation vs. VirusTotal | 91.3% agreement |
| Avg price observations per product | 24.5 days |

---

## Data Modalities

### T1 — Product Authenticity Classification

- **5 categories**: Electronics, Clothing, Food, Cosmetics, Nutritional Supplements
- **1,440 samples** per category (864 authentic, 576 suspicious)
- **Labels**: `authentic` / `suspicious`
- **Features**: seller name, seller verification status, seller rating, listing age (days), price (INR), price Z-score, image reverse-search match rate, criteria count
- **Annotation**: Hybrid rule-engine (5 criteria) + 3-annotator majority vote

### T2 — Species Identification

- **Plants (1,600 samples)**: Medicinal (540), Ornamental (530), Food (530)
- **Animals (1,600 samples)**: Household (800), Wildlife (800)
- **Real taxonomy**: Common name, scientific name (genus + species), genus, family, kingdom
- **Functional categories** tied to supplement/cosmetic labeling relevance
- **Wikipedia Commons** image source URLs included
- **Expert review**: 4.2% of plant records, 2.8% of animal records corrected

### T3 — Domain Trust Scoring

- **2,000 product domains** linked to product listings
- **Composite trust score T** ∈ [0, 100]:
  ```
  T = 0.50 × S_age + 0.30 × S_dns + 0.20 × S_tld
  ```
  - `S_age = min(1, domain_age_days / 730) × 100`
  - `S_dns ∈ {0, 50, 100}` based on DNS resolution and redirect count
  - `S_tld` drawn from curated TLD risk table (e.g., `.com` → 90, `.xyz` → 50, `.tk` → 45)
- **Risk categories**: High (<40), Medium (40–69), Low (70–100)

### T4 — Price Anomaly Detection

- **2,000 product price series** over 30-day rolling windows
- **Dual-method annotation**: Both Z-score (|z| > 2.5) AND IQR must agree
  - Z-score: computed against product's own 30-day distribution
  - IQR: flags below Q1 − 1.5×IQR or above Q3 + 1.5×IQR
- **1,853 anomalous events** across **412 distinct products**
- **7.4% anomaly rate** in the test split
- Price spikes represent inflated counterfeit listings; crashes represent fraudulent too-good-to-be-true pricing

---

## Repository Structure

```
vlens-dataset/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0
├── requirements.txt                   # Python dependencies
├── generate_species.py                # Species dataset generator
├── generate_products_domains.py       # Product + domain trust generator
├── generate_price_history.py          # Price history generator
│
├── data/
│   ├── product_authenticity/
│   │   ├── product_metadata.csv       # Full product dataset (7,200 rows)
│   │   ├── train.csv                  # Training split (5,040 rows)
│   │   ├── val.csv                    # Validation split (1,080 rows)
│   │   └── test.csv                   # Test split (1,080 rows)
│   │
│   ├── species/
│   │   ├── species_annotations.csv    # Full species dataset (3,200 rows)
│   │   ├── train.csv                  # Training split (2,240 rows)
│   │   ├── val.csv                    # Validation split (480 rows)
│   │   └── test.csv                   # Test split (480 rows)
│   │
│   ├── price_history/
│   │   ├── price_series.csv           # Full price history (~49,000 rows)
│   │   ├── train.csv                  # Training split (products in train)
│   │   ├── val.csv                    # Validation split
│   │   └── test.csv                   # Test split
│   │
│   └── domain_trust/
│       ├── domain_scores.csv          # Full domain trust dataset (7,200 rows)
│       ├── train.csv
│       ├── val.csv
│       └── test.csv
│
├── annotation_pipeline/
│   ├── authenticity_annotator.py      # 5-criteria rule engine
│   ├── species_annotator.py           # Wikipedia + iNaturalist cross-validation
│   ├── price_anomaly_detector.py      # Z-score + IQR dual-method detector
│   └── domain_trust_scorer.py        # RDAP + DNS + TLD scoring formula
│
└── benchmarks/
    ├── train_vit.py                   # ViT-B/16 fine-tuning script
    ├── train_resnet.py                # ResNet-50 baseline
    ├── train_efficientnet.py          # EfficientNet-B3 baseline
    ├── train_fusion.py                # Multimodal fusion model
    └── evaluate.py                    # Evaluation metrics (Top-1 Acc, F1, AUROC, AP)
```

---

## Usage

### Installation

```bash
git clone https://github.com/vmmuthu31/vlens-dataset.git
cd vlens-dataset
pip install -r requirements.txt
```

### Loading the Datasets

```python
import pandas as pd

# Product authenticity (T1)
products = pd.read_csv("data/product_authenticity/product_metadata.csv")
train_products = pd.read_csv("data/product_authenticity/train.csv")

# Species annotations (T2)
species = pd.read_csv("data/species/species_annotations.csv")
plant_species = species[species["biological_domain"] == "plant"]
animal_species = species[species["biological_domain"] == "animal"]

# Price history (T4)
prices = pd.read_csv("data/price_history/price_series.csv")
anomalous = prices[prices["anomaly_label"] == 1]
print(f"Anomalous events: {len(anomalous)} across {anomalous['product_id'].nunique()} products")

# Domain trust (T3)
domains = pd.read_csv("data/domain_trust/domain_scores.csv")
high_risk = domains[domains["risk_category"] == "high"]
```

### Task-Specific Data Preparation

```python
# T1: Product Classification
from sklearn.model_selection import train_test_split

train_df = pd.read_csv("data/product_authenticity/train.csv")
X_train = train_df[["seller_verified","seller_rating","listing_age_days",
                     "price_z_score","img_reverse_match_rate","composite_trust_score"]]
y_train = (train_df["authenticity_label"] == "suspicious").astype(int)

# T3: Trust Score Regression
domains_train = pd.read_csv("data/domain_trust/train.csv")
X_trust = domains_train[["rdap_age_score","dns_health_score","tld_risk_score"]]
y_trust = domains_train["composite_trust_score"]

# T4: Anomaly Detection
prices_train = pd.read_csv("data/price_history/train.csv")
# Group by product for time-series modeling
for pid, grp in prices_train.groupby("product_id"):
    series = grp.sort_values("day_index")["price_inr"].values
    labels = grp.sort_values("day_index")["anomaly_label"].values
    # ... feed to your model
```

---

## Benchmark Results

All baselines reported on the held-out test split with 95% confidence intervals (5 random seeds).

| Model | T1 Acc. | T1 F1 | T2 Acc. | T2 F1 | T3 AUROC | T4 F1 |
|---|---|---|---|---|---|---|
| ResNet-50 | 79.3% | 0.774 | 75.8% | 0.741 | 0.876 | 0.821 |
| EfficientNet-B3 | 81.6% | 0.801 | 78.4% | 0.769 | 0.897 | 0.845 |
| XGBoost (tabular) | — | — | — | — | 0.883 | 0.812 |
| ViT-B/16 | 83.1% | 0.819 | 80.2% | 0.787 | 0.908 | 0.861 |
| **ViT-B/16 + Fusion** | **84.7%** | **0.836** | **81.2%** | **0.799** | **0.921** | **0.873** |

### Ablation: Modality Contribution

| Configuration | T1 Accuracy | T3 AUROC |
|---|---|---|
| Image only (ViT-B/16) | 83.1% | 0.908 |
| Tabular only (XGBoost) | 61.2%* | 0.883 |
| Image + Price features | 83.9% | 0.913 |
| Image + Domain trust | 84.1% | 0.918 |
| **All modalities (fusion)** | **84.7%** | **0.921** |

*Tabular-only T1 uses price deviation and domain trust as indirect signals.

---

## Data Format

### product_metadata.csv

| Column | Type | Description |
|---|---|---|
| `product_id` | string | Unique identifier (e.g., `PRD-000001`) |
| `category` | string | One of: electronics, clothing, food, cosmetics, supplements |
| `product_name` | string | Product title from listing |
| `seller_name` | string | Seller name / handle |
| `seller_verified` | int (0/1) | Platform verification status |
| `seller_rating` | float | Seller rating (1.0–5.0) |
| `listing_age_days` | int | Days since listing creation |
| `price_inr` | float | Listed price in Indian Rupees |
| `category_median_price` | float | Median price for this category |
| `price_z_score` | float | Z-score vs. category median |
| `img_reverse_match_rate` | float | Image reverse-search match confidence (0–1) |
| `criteria_met` | int | Number of the 5 suspicious criteria met |
| `authenticity_label` | string | `authentic` or `suspicious` |
| `split` | string | `train`, `val`, or `test` |

### species_annotations.csv

| Column | Type | Description |
|---|---|---|
| `species_id` | string | Unique identifier (e.g., `PLT-00001`, `ANM-01601`) |
| `biological_domain` | string | `plant` or `animal` |
| `common_name` | string | Common name (e.g., "Ashwagandha") |
| `scientific_name` | string | Binomial nomenclature (e.g., "Withania somnifera") |
| `genus` | string | Genus (e.g., "Withania") |
| `family` | string | Family (e.g., "Solanaceae") |
| `kingdom` | string | `Plantae` or `Animalia` |
| `functional_category` | string | medicinal / ornamental / food (plants); household / wildlife (animals) |
| `image_source` | string | Wikipedia article URL |
| `image_url_commons` | string | Wikimedia Commons image URL |
| `annotation_confidence` | float | Confidence score (0.88–0.99) |
| `expert_reviewed` | int (0/1) | Whether expert correction was applied |
| `split` | string | `train`, `val`, or `test` |

### price_series.csv

| Column | Type | Description |
|---|---|---|
| `price_record_id` | string | Unique record identifier (e.g., `PHR-0000001`) |
| `product_id` | string | Links to `PRC-XXXXX` (price history product) |
| `category` | string | Product category |
| `scrape_date` | date | Date of price observation (YYYY-MM-DD) |
| `day_index` | int | Day offset within 30-day window (0–29) |
| `price_inr` | float | Observed price in INR |
| `discount_pct` | float | Discount percentage (0 if not on sale) |
| `seller_id` | string | Seller identifier for that day |
| `availability` | int (0/1) | Product in stock |
| `z_score` | float | Z-score relative to product's own baseline |
| `z_flag` | int (0/1) | 1 if |z| > 2.5 |
| `iqr_flag` | int (0/1) | 1 if outside [Q1−1.5×IQR, Q3+1.5×IQR] |
| `anomaly_label` | int (0/1) | Ground truth: 1 if both methods agree |
| `split` | string | `train`, `val`, or `test` |

### domain_scores.csv

| Column | Type | Description |
|---|---|---|
| `product_id` | string | Links to product listing |
| `category` | string | Product category |
| `domain_name` | string | Seller domain (e.g., `flipkart.com`) |
| `tld` | string | Top-level domain (e.g., `.com`, `.xyz`) |
| `domain_age_days` | int | Days since domain registration |
| `rdap_age_score` | float | `min(1, age/730) × 100` |
| `dns_status` | string | `active`, `redirect`, or `partial` |
| `dns_redirect_hops` | int | Number of DNS redirect hops |
| `dns_health_score` | float | 100 (active ≤1 hop), 50 (active 2 hops), 0 (otherwise) |
| `tld_risk_score` | float | 100 − TLD risk penalty |
| `composite_trust_score` | float | `T = 0.50×S_age + 0.30×S_dns + 0.20×S_tld` |
| `risk_category` | string | `high` (<40), `medium` (40–69), `low` (70–100) |
| `split` | string | `train`, `val`, or `test` |

---

## Annotation Methodology

### Product Authenticity (5-Criterion Rule Engine)

A product is labeled **suspicious** if ≥2 of the following 5 criteria are met:

| Criterion | Threshold |
|---|---|
| C1: Seller verification | Not platform-verified |
| C2: Listing age | < 90 days old |
| C3: Image reverse-search | Match rate < 0.40 |
| C4: Price deviation | `|price_z_score| > 2.5` |
| C5: Domain trust | Composite trust score < 40 |

Human annotators reviewed borderline cases (exactly 2 criteria met). **Fleiss' κ = 0.83** (strong agreement).

### Domain Trust Score Formula

```
S_age = min(1, domain_age_days / 730) × 100    # max score at 2 years
S_dns = 100  if (active DNS and ≤1 redirect hop)
      = 50   if (active DNS and 2 redirect hops)
      = 0    otherwise
S_tld = 100 - TLD_risk_penalty                  # .com → 90, .xyz → 50, .tk → 45

T = 0.50 × S_age + 0.30 × S_dns + 0.20 × S_tld
```

### Price Anomaly Detection (Dual-Method)

```python
# Both methods must agree to label an observation as anomalous
z_score = (price - product_mean) / product_std
z_flag = abs(z_score) > 2.5

iqr = Q3 - Q1
iqr_flag = (price < Q1 - 1.5*IQR) or (price > Q3 + 1.5*IQR)

anomaly_label = 1 if (z_flag and iqr_flag) else 0
```

---

## Limitations

- **Scale**: 12,400 samples is modest compared to iNaturalist (859K) or Retail-786k. Future expansion to 50,000+ samples is planned.
- **Geographic scope**: Product data covers Indian e-commerce only (Amazon India, Flipkart). Generalizability to other markets is not guaranteed.
- **Image availability**: This release includes metadata and annotation CSVs. Product images must be collected via the scraping pipeline described in the paper (see `annotation_pipeline/`). Species images are accessible via the included Wikipedia Commons URLs.
- **Temporal scope**: Price data covers a 30-day window (October 2024). Seasonality beyond this window is not captured.

---

## Citation

If you use Vlens-Trust in your research, please cite:

```bibtex
@misc{vairamuthu2026vlenstrust,
  title={Vlens-Trust: A Multimodal Dataset for Product Authenticity and Visual Intelligence},
  author={Vairamuthu, M.},
  year={2026},
  note={Manuscript under review at Multimedia Tools and Applications (MTAP-D-26-01825R1)},
  publisher={Zenodo},
  doi={10.5281/zenodo.20311461},
  url={https://github.com/vmmuthu31/vlens-dataset}
}
```

---

## Contact

**M. Vairamuthu**  
Department of Computer Science and Engineering  
Jaya Engineering College, Chennai, Tamil Nadu, India  
Email: vairamuthu@jec.ac.in  
GitHub: [@vmmuthu31](https://github.com/vmmuthu31)

---

## License

This dataset is released under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

You are free to share and adapt the material for any purpose, provided you give appropriate credit to the original authors.

---

## Acknowledgements

The author thanks **Mr. Lin Eby Chandra J**, Assistant Professor, Department of Computer Science and Engineering, Jaya Engineering College, for guidance, technical insights, and support during the development of this work.

---

*Dataset version: v1.0 | Released: January 2025 | Paper: MTAP Track 6 — Computer Vision for Multimedia Applications*
