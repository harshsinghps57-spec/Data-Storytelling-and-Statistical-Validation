"""
Week 4 Task: Hypothesis Testing & Statistical Validation
Tests:
1. T-test: Do different customer segments have significantly different profit margins?
2. ANOVA: Are there significant differences in sales across regions?
3. Chi-Square: Is there a relationship between ship mode and region?
4. Correlation Analysis: Sales vs Profit, Discount vs Profit
5. Normality Test: Shapiro-Wilk on profit distribution
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Data-Storytelling-and-Statistical-Validation"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().replace(' ', '_') for c in df.columns]

print("=" * 65)
print("       WEEK 4: STATISTICAL VALIDATION & HYPOTHESIS TESTING")
print("=" * 65)

report_lines = []
report_lines.append("# Week 4: Statistical Validation & Hypothesis Testing\n")
report_lines.append(f"Dataset: {len(df)} rows, {len(df.columns)} columns\n")

# ── 1. Normality Test on Profit ──────────────────────────────────────────────
print("\n[1] NORMALITY TEST: Profit Distribution (Shapiro-Wilk)")
sample = df['Profit'].dropna().sample(min(5000, len(df)), random_state=42)
stat_sw, p_sw = stats.shapiro(sample)
report_lines.append("## 1. Normality Test (Shapiro-Wilk) - Profit\n")
report_lines.append(f"- **H0**: Profit is normally distributed  ")
report_lines.append(f"- **Test Statistic (W)**: {stat_sw:.4f}  ")
report_lines.append(f"- **p-value**: {p_sw:.6f}  ")
if p_sw < 0.05:
    conclusion = "**Result**: Reject H0 - Profit is NOT normally distributed (p < 0.05)"
else:
    conclusion = "**Result**: Fail to reject H0 - Profit appears normally distributed (p >= 0.05)"
report_lines.append(f"- {conclusion}\n")
print(f"   W = {stat_sw:.4f}, p = {p_sw:.6f}")
print(f"   -> {conclusion.replace('**','')}")

# ── 2. T-Test: Consumer vs Corporate Profit Margin ───────────────────────────
print("\n[2] INDEPENDENT T-TEST: Consumer vs Corporate Profit Margin")
t_stat = 0.0; p_t = 1.0
if 'Segment' in df.columns and 'Profit' in df.columns and 'Sales' in df.columns:
    df['Profit_Margin'] = df['Profit'] / df['Sales'].replace(0, np.nan)
    consumer = df[df['Segment'] == 'Consumer']['Profit_Margin'].dropna()
    corporate = df[df['Segment'] == 'Corporate']['Profit_Margin'].dropna()
    t_stat, p_t = stats.ttest_ind(consumer, corporate)
    report_lines.append("## 2. Independent T-Test - Consumer vs Corporate Profit Margin\n")
    report_lines.append(f"- **H0**: Mean profit margin is equal for Consumer and Corporate segments  ")
    report_lines.append(f"- **Consumer Mean**: {consumer.mean():.4f} | **Corporate Mean**: {corporate.mean():.4f}  ")
    report_lines.append(f"- **t-statistic**: {t_stat:.4f}  ")
    report_lines.append(f"- **p-value**: {p_t:.6f}  ")
    if p_t < 0.05:
        concl = "**Result**: Reject H0 - Profit margins differ significantly between Consumer & Corporate (p < 0.05)"
    else:
        concl = "**Result**: Fail to reject H0 - No significant difference in profit margins (p >= 0.05)"
    report_lines.append(f"- {concl}\n")
    print(f"   t = {t_stat:.4f}, p = {p_t:.6f}")
    print(f"   Consumer mean = {consumer.mean():.4f}, Corporate mean = {corporate.mean():.4f}")
    print(f"   -> {concl.replace('**','')}")

# ── 3. One-Way ANOVA: Sales across Regions ───────────────────────────────────
print("\n[3] ONE-WAY ANOVA: Sales across Regions")
f_stat = 0.0; p_anova = 1.0
if 'Region' in df.columns:
    region_groups = [group['Sales'].dropna().values for _, group in df.groupby('Region')]
    f_stat, p_anova = stats.f_oneway(*region_groups)
    region_means = df.groupby('Region')['Sales'].mean().round(2)
    report_lines.append("## 3. One-Way ANOVA - Sales across Regions\n")
    report_lines.append(f"- **H0**: Mean sales is equal across all regions  ")
    report_lines.append(f"- **F-statistic**: {f_stat:.4f}  ")
    report_lines.append(f"- **p-value**: {p_anova:.6f}  ")
    report_lines.append("- **Region Mean Sales**:  \n")
    for region, mean_val in region_means.items():
        report_lines.append(f"  - {region}: ${mean_val:,.2f}")
    if p_anova < 0.05:
        concl3 = "**Result**: Reject H0 - Significant sales differences exist across regions (p < 0.05)"
    else:
        concl3 = "**Result**: Fail to reject H0 - No significant difference in sales across regions (p >= 0.05)"
    report_lines.append(f"\n- {concl3}\n")
    print(f"   F = {f_stat:.4f}, p = {p_anova:.6f}")
    print(f"   -> {concl3.replace('**','')}")

# ── 4. Chi-Square: Ship Mode vs Region ───────────────────────────────────────
print("\n[4] CHI-SQUARE TEST: Ship Mode vs Region")
chi2 = 0.0; p_chi = 1.0
if 'Ship_Mode' in df.columns and 'Region' in df.columns:
    ct = pd.crosstab(df['Ship_Mode'], df['Region'])
    chi2, p_chi, dof, expected = stats.chi2_contingency(ct)
    report_lines.append("## 4. Chi-Square Test - Ship Mode vs Region\n")
    report_lines.append(f"- **H0**: Ship mode is independent of region  ")
    report_lines.append(f"- **Chi-Square Statistic**: {chi2:.4f}  ")
    report_lines.append(f"- **Degrees of Freedom**: {dof}  ")
    report_lines.append(f"- **p-value**: {p_chi:.6f}  ")
    if p_chi < 0.05:
        concl4 = "**Result**: Reject H0 - Ship mode and region are NOT independent (p < 0.05)"
    else:
        concl4 = "**Result**: Fail to reject H0 - Ship mode appears independent of region (p >= 0.05)"
    report_lines.append(f"- {concl4}\n")
    print(f"   chi2 = {chi2:.4f}, dof = {dof}, p = {p_chi:.6f}")
    print(f"   -> {concl4.replace('**','')}")

# ── 5. Pearson Correlation ───────────────────────────────────────────────────
print("\n[5] PEARSON CORRELATION ANALYSIS")
report_lines.append("## 5. Pearson Correlation Analysis\n")
pairs = [('Sales', 'Profit'), ('Discount', 'Profit'), ('Quantity', 'Profit')]
corr_results = {}
for col_a, col_b in pairs:
    if col_a in df.columns and col_b in df.columns:
        r, p_corr = stats.pearsonr(df[col_a].dropna(), df[col_b].dropna())
        strength = "strong" if abs(r) > 0.5 else ("moderate" if abs(r) > 0.3 else "weak")
        direction = "positive" if r > 0 else "negative"
        corr_results[f"{col_a}_vs_{col_b}"] = (r, p_corr)
        report_lines.append(f"### {col_a} vs {col_b}")
        report_lines.append(f"- r = **{r:.4f}**, p = {p_corr:.6f}")
        report_lines.append(f"- Interpretation: {strength} {direction} correlation\n")
        print(f"   {col_a} vs {col_b}: r = {r:.4f}, p = {p_corr:.6f} -> {strength} {direction}")

# ── Save Report ──────────────────────────────────────────────────────────────
report_path = os.path.join(OUTPUT_DIR, "statistical_tests_report.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))
print(f"\n[OK] Statistical report saved to: {report_path}")

# ── Save Summary CSV ─────────────────────────────────────────────────────────
summary_df = pd.DataFrame({
    "Test": [
        "Shapiro-Wilk (Profit Normality)",
        "T-Test (Consumer vs Corporate)",
        "ANOVA (Sales by Region)",
        "Chi-Square (Ship Mode vs Region)"
    ],
    "Statistic": [round(stat_sw, 4), round(t_stat, 4), round(f_stat, 4), round(chi2, 4)],
    "p-value": [round(p_sw, 6), round(p_t, 6), round(p_anova, 6), round(p_chi, 6)],
    "Significant_at_0.05": [p_sw < 0.05, p_t < 0.05, p_anova < 0.05, p_chi < 0.05],
    "Decision": [
        "Reject H0" if p_sw < 0.05 else "Fail to Reject",
        "Reject H0" if p_t < 0.05 else "Fail to Reject",
        "Reject H0" if p_anova < 0.05 else "Fail to Reject",
        "Reject H0" if p_chi < 0.05 else "Fail to Reject"
    ]
})
summary_df.to_csv(os.path.join(OUTPUT_DIR, "hypothesis_test_results.csv"), index=False)
print("[OK] Summary CSV saved.")
print("\n" + "=" * 65)
print("ALL HYPOTHESIS TESTS COMPLETE")
print("=" * 65)
