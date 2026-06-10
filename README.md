# Week 4: Data Storytelling & Statistical Validation 📊

## Overview
This project is **Week 4** of my Data Analytics Internship. The goal is to transform raw data insights from previous weeks into compelling **data narratives** and validate findings using **statistical hypothesis testing**.

## 🎯 Objectives
- Craft **5 data stories** from the Superstore dataset
- Apply **4 hypothesis tests** to statistically validate findings
- Measure **3 Pearson correlations** for key variable relationships
- Build an interactive **HTML presentation** for storytelling

## 📁 Project Structure
```
Data-Storytelling-and-Statistical-Validation/
│
├── data/
│   └── cleaned_superstore.csv          # Dataset (from Week 2 EDA)
│
├── src/
│   ├── hypothesis_testing.py           # All statistical hypothesis tests
│   └── data_storytelling.py           # Story-driven chart generation
│
├── output/
│   ├── charts/                         # All generated story charts
│   │   ├── story1_discount_trap.png
│   │   ├── story2_regional_performance.png
│   │   ├── story3_category_profitability.png
│   │   ├── story4_stats_dashboard.png
│   │   └── story5_growth_narrative.png
│   ├── statistical_tests_report.md     # Detailed hypothesis test results
│   └── hypothesis_test_results.csv     # Structured results table
│
└── presentation/
    └── index.html                      # Interactive HTML Data Story Presentation
```

## 📖 The 5 Data Stories

| # | Story | Key Finding |
|---|-------|-------------|
| 1 | 🎯 **The Discount Trap** | Discounts >40% consistently cause losses (r = −0.22) |
| 2 | 🗺️ **Regional Disparity** | West leads; Central struggles (ANOVA: p < 0.05) |
| 3 | 💡 **Technology Dominates** | Tech = 50% of profit; Furniture = hidden loss center |
| 4 | 📊 **Profit is Not Normal** | Shapiro-Wilk: W=0.663, p < 0.001 — heavy skew |
| 5 | 📈 **Sales Are Growing** | YoY +20% sales, but profit growth is lagging |

## 🧪 Statistical Tests Applied

| Test | Variable(s) | Result |
|------|-------------|--------|
| **Shapiro-Wilk** | Profit distribution | ❌ Reject H₀ — NOT normally distributed |
| **Independent T-Test** | Consumer vs Corporate profit margin | ❌ Reject H₀ — Significant difference |
| **One-Way ANOVA** | Sales across Regions | ❌ Reject H₀ — Regions differ significantly |
| **Chi-Square** | Ship Mode vs Region | ❌ Reject H₀ — NOT independent |

## 🔗 Pearson Correlations

| Pair | r Value | Interpretation |
|------|---------|----------------|
| Sales vs Profit | +0.48 | Moderate positive — more sales → more profit |
| Discount vs Profit | −0.22 | Weak negative — discounts erode profit |
| Quantity vs Profit | +0.07 | Very weak — volume has minimal impact |

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy scipy matplotlib seaborn
```

### Run Statistical Tests
```bash
python src/hypothesis_testing.py
```

### Generate Story Charts
```bash
python src/data_storytelling.py
```

### View Presentation
Open `presentation/index.html` in any web browser.

## 💡 Business Recommendations

1. **Cap discounts at 30%** — statistical evidence confirms higher discounts erode all profit
2. **Invest in West, fix Central** — ANOVA confirms regional performance gaps are real
3. **Prioritize Technology** — highest profit margin category by far
4. **Audit Furniture SKUs** — Tables and Bookcases consistently lose money
5. **Manage Q4 discounting** — seasonal promotions spike sales but crash margins
6. **Optimize shipping by region** — Chi-square confirms regional shipping dependency

## 🛠️ Tools & Technologies
- **Python 3** — Data processing and statistical analysis
- **SciPy** — Hypothesis testing (shapiro, ttest_ind, f_oneway, chi2_contingency, pearsonr)
- **Pandas & NumPy** — Data manipulation
- **Matplotlib & Seaborn** — Data visualization
- **HTML5 / CSS3 / JavaScript** — Interactive presentation

## 📊 Dataset
- **Source**: Sample - Superstore (Tableau Public Dataset)
- **Rows**: 9,994 orders
- **Period**: 2014–2017
- **Features**: Order details, product categories, sales, profit, discount, region, segment

---
*Internship Week 4 Task — Data Analytics Program*
