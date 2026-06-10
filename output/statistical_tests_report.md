# Week 4: Statistical Validation & Hypothesis Testing

Dataset: 9994 rows, 27 columns

## 1. Normality Test (Shapiro-Wilk) - Profit

- **H0**: Profit is normally distributed  
- **Test Statistic (W)**: 0.2492  
- **p-value**: 0.000000  
- **Result**: Reject H0 - Profit is NOT normally distributed (p < 0.05)

## 2. Independent T-Test - Consumer vs Corporate Profit Margin

- **H0**: Mean profit margin is equal for Consumer and Corporate segments  
- **Consumer Mean**: 0.1120 | **Corporate Mean**: 0.1212  
- **t-statistic**: -0.8462  
- **p-value**: 0.397479  
- **Result**: Fail to reject H0 - No significant difference in profit margins (p >= 0.05)

## 3. One-Way ANOVA - Sales across Regions

- **H0**: Mean sales is equal across all regions  
- **F-statistic**: 0.8006  
- **p-value**: 0.493320  
- **Region Mean Sales**:  

  - Central: $215.77
  - East: $238.34
  - South: $241.80
  - West: $226.49

- **Result**: Fail to reject H0 - No significant difference in sales across regions (p >= 0.05)

## 4. Chi-Square Test - Ship Mode vs Region

- **H0**: Ship mode is independent of region  
- **Chi-Square Statistic**: 23.8462  
- **Degrees of Freedom**: 9  
- **p-value**: 0.004551  
- **Result**: Reject H0 - Ship mode and region are NOT independent (p < 0.05)

## 5. Pearson Correlation Analysis

### Sales vs Profit
- r = **0.4791**, p = 0.000000
- Interpretation: moderate positive correlation

### Discount vs Profit
- r = **-0.2195**, p = 0.000000
- Interpretation: weak negative correlation

### Quantity vs Profit
- r = **0.0663**, p = 0.000000
- Interpretation: weak positive correlation
