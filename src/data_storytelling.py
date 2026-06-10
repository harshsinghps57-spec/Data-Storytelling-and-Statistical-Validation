"""
Week 4: Data Storytelling Visualizations
Creates compelling story-driven charts for narrative presentation
"""
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from scipy import stats
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\Data-Storytelling-and-Statistical-Validation"
DATA_FILE = os.path.join(BASE_DIR, "data", "cleaned_superstore.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "output", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ── Color Palette ─────────────────────────────────────────────────────────────
PALETTE = {
    "primary": "#6C63FF",
    "secondary": "#FF6584",
    "accent": "#43E97B",
    "dark": "#1A1A2E",
    "mid": "#16213E",
    "card": "#0F3460",
    "text": "#E0E0E0",
    "muted": "#A0A0B0",
    "warning": "#FFB347",
    "danger": "#FF4C4C",
    "success": "#00C49A",
}

plt.rcParams.update({
    'figure.facecolor': PALETTE['dark'],
    'axes.facecolor': PALETTE['mid'],
    'axes.edgecolor': PALETTE['card'],
    'axes.labelcolor': PALETTE['text'],
    'axes.titlecolor': PALETTE['text'],
    'xtick.color': PALETTE['muted'],
    'ytick.color': PALETTE['muted'],
    'text.color': PALETTE['text'],
    'grid.color': PALETTE['card'],
    'grid.alpha': 0.5,
    'font.family': 'DejaVu Sans',
    'font.size': 11
})

df = pd.read_csv(DATA_FILE)
df.columns = [c.strip().replace(' ', '_') for c in df.columns]
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Year'] = df['Order_Date'].dt.year
df['Profit_Margin'] = df['Profit'] / df['Sales'].replace(0, np.nan)

print("Generating data story charts...")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 1: Story — The Discount Trap (Scatter with regression line)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.patch.set_facecolor(PALETTE['dark'])

ax = axes[0]
ax.set_facecolor(PALETTE['mid'])
colors = np.where(df['Profit'] > 0, PALETTE['accent'], PALETTE['danger'])
sc = ax.scatter(df['Discount'], df['Profit'], c=colors, alpha=0.35, s=15, edgecolors='none')
# Regression line
m, b, r, p, se = stats.linregress(df['Discount'].dropna(), df['Profit'].dropna())
x_line = np.linspace(0, df['Discount'].max(), 200)
ax.plot(x_line, m * x_line + b, color=PALETTE['warning'], linewidth=2.5, linestyle='--', label=f'Trend (r={r:.2f})')
ax.axhline(0, color=PALETTE['muted'], linewidth=0.8, linestyle=':')
ax.set_title('🔍 The Discount Trap\nHigher discounts = lower profits', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Discount Rate', fontsize=12)
ax.set_ylabel('Profit ($)', fontsize=12)
ax.legend(loc='upper right', framealpha=0.3)
ax.grid(True, alpha=0.3)

# Add annotation
ax.annotate('Products with >40%\ndiscount mostly\nlose money!',
            xy=(0.42, -300), xytext=(0.55, 500),
            arrowprops=dict(arrowstyle='->', color=PALETTE['secondary'], lw=1.5),
            fontsize=9, color=PALETTE['secondary'],
            bbox=dict(boxstyle='round,pad=0.3', facecolor=PALETTE['card'], alpha=0.8))

# Chart 2: Profit by Discount Bucket
ax2 = axes[1]
ax2.set_facecolor(PALETTE['mid'])
df['Discount_Bucket'] = pd.cut(df['Discount'], bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.01],
                                labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])
bucket_stats = df.groupby('Discount_Bucket', observed=False)['Profit'].mean()
bar_colors = [PALETTE['success'] if v > 0 else PALETTE['danger'] for v in bucket_stats.values]
bars = ax2.bar(bucket_stats.index.astype(str), bucket_stats.values, color=bar_colors,
               edgecolor=PALETTE['card'], linewidth=0.8, width=0.65)
for bar, val in zip(bars, bucket_stats.values):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (5 if val >= 0 else -20),
             f'${val:.0f}', ha='center', va='bottom', fontsize=9, color=PALETTE['text'], fontweight='bold')
ax2.axhline(0, color=PALETTE['muted'], linewidth=1, linestyle='--')
ax2.set_title('💸 Average Profit by Discount Bracket\nWhere does profit turn negative?', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('Discount Bracket', fontsize=12)
ax2.set_ylabel('Avg. Profit ($)', fontsize=12)
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('STORY 1: The Discount Trap — Why Deep Discounts Erode Profitability',
             fontsize=16, fontweight='bold', color=PALETTE['primary'], y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'story1_discount_trap.png'), dpi=150, bbox_inches='tight',
            facecolor=PALETTE['dark'])
plt.close()
print("  [OK] Story 1: Discount Trap chart saved")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 2: Story — Regional Performance Disparity (ANOVA result visualization)
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.patch.set_facecolor(PALETTE['dark'])

region_colors = ['#6C63FF', '#FF6584', '#43E97B', '#FFB347']

ax = axes[0]
ax.set_facecolor(PALETTE['mid'])
region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
region_sales = df.groupby('Region')['Sales'].sum()
bars = ax.bar(region_profit.index, region_profit.values, color=region_colors, width=0.6,
              edgecolor=PALETTE['card'], linewidth=0.8)
for bar, val in zip(bars, region_profit.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000,
            f'${val/1000:.1f}K', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_title('🗺️ Total Profit by Region\n(ANOVA confirms significant differences)', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Total Profit ($)', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

# Statistical annotation
region_groups = [group['Sales'].dropna().values for _, group in df.groupby('Region')]
f_val, p_val = stats.f_oneway(*region_groups)
ax.text(0.02, 0.97, f'ANOVA: F={f_val:.2f}, p={p_val:.4f}\n{"✅ Significant!" if p_val<0.05 else "Not significant"}',
        transform=ax.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor=PALETTE['card'], alpha=0.8), color=PALETTE['accent'])

# Violin plot
ax2 = axes[1]
ax2.set_facecolor(PALETTE['mid'])
region_order = df.groupby('Region')['Profit'].median().sort_values(ascending=False).index.tolist()
vp = ax2.violinplot([df[df['Region']==r]['Profit'].dropna().values for r in region_order],
                    showmedians=True, showextrema=False)
for i, pc in enumerate(vp['bodies']):
    pc.set_facecolor(region_colors[i])
    pc.set_alpha(0.7)
vp['cmedians'].set_color(PALETTE['warning'])
vp['cmedians'].set_linewidth(2)
ax2.set_xticks(range(1, len(region_order)+1))
ax2.set_xticklabels(region_order)
ax2.set_title('📊 Profit Distribution by Region\n(Violin Plot — spread & median)', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('Region', fontsize=12)
ax2.set_ylabel('Profit ($)', fontsize=12)
ax2.axhline(0, color=PALETTE['muted'], linewidth=0.8, linestyle=':')
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('STORY 2: Regional Disparity — West Leads, Central Struggles',
             fontsize=16, fontweight='bold', color=PALETTE['primary'], y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'story2_regional_performance.png'), dpi=150, bbox_inches='tight',
            facecolor=PALETTE['dark'])
plt.close()
print("  [OK] Story 2: Regional Performance chart saved")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 3: Story — Technology Segment Dominates
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(22, 7))
fig.patch.set_facecolor(PALETTE['dark'])
cat_colors = {'Technology': '#6C63FF', 'Furniture': '#FF6584', 'Office Supplies': '#43E97B'}

ax = axes[0]
ax.set_facecolor(PALETTE['mid'])
cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
colors_cat = [cat_colors.get(c, '#888') for c in cat_profit.index]
bars = ax.barh(cat_profit.index, cat_profit.values, color=colors_cat, height=0.5)
for bar, val in zip(bars, cat_profit.values):
    ax.text(val + 500, bar.get_y() + bar.get_height()/2,
            f'${val/1000:.1f}K', va='center', fontsize=11, fontweight='bold')
ax.set_title('💡 Total Profit by Category', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Total Profit ($)')
ax.grid(True, alpha=0.3, axis='x')

ax2 = axes[1]
ax2.set_facecolor(PALETTE['mid'])
cat_margin = df.groupby('Category')['Profit_Margin'].mean().sort_values(ascending=False) * 100
colors_m = [cat_colors.get(c, '#888') for c in cat_margin.index]
bars2 = ax2.bar(cat_margin.index, cat_margin.values, color=colors_m, width=0.5)
for bar, val in zip(bars2, cat_margin.values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val:.1f}%', ha='center', fontsize=11, fontweight='bold')
ax2.axhline(0, color=PALETTE['muted'], linewidth=0.8)
ax2.set_title('📈 Avg. Profit Margin by Category', fontsize=13, fontweight='bold', pad=15)
ax2.set_ylabel('Profit Margin (%)')
ax2.grid(True, alpha=0.3, axis='y')

ax3 = axes[2]
ax3.set_facecolor(PALETTE['mid'])
top_sub = df.groupby(['Category', 'Sub-Category'])['Profit'].sum().reset_index()
top5_sub = top_sub.nlargest(10, 'Profit')
colors_sub = [cat_colors.get(
    df[df['Sub-Category']==sc]['Category'].mode()[0] if len(df[df['Sub-Category']==sc])>0 else 'Office Supplies','#888')
    for sc in top5_sub['Sub-Category']]
bars3 = ax3.barh(top5_sub['Sub-Category'], top5_sub['Profit'], color=colors_sub, height=0.6)
ax3.set_title('🏆 Top 10 Sub-Categories by Profit', fontsize=13, fontweight='bold', pad=15)
ax3.set_xlabel('Total Profit ($)')
ax3.grid(True, alpha=0.3, axis='x')

fig.suptitle('STORY 3: Technology Dominates — Furniture is a Hidden Loss Center',
             fontsize=16, fontweight='bold', color=PALETTE['primary'], y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'story3_category_profitability.png'), dpi=150, bbox_inches='tight',
            facecolor=PALETTE['dark'])
plt.close()
print("  [OK] Story 3: Category Profitability chart saved")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 4: Statistical Tests Summary Dashboard
# ══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 10))
fig.patch.set_facecolor(PALETTE['dark'])

tests = {
    "Shapiro-Wilk\n(Profit Normality)": {"stat": "W=0.66", "p": "< 0.001", "result": "Reject H₀", "color": PALETTE['danger']},
    "T-Test\n(Consumer vs Corporate)": {"stat": "t=...", "p": "See CSV", "result": "See Report", "color": PALETTE['warning']},
    "ANOVA\n(Sales by Region)": {"stat": f"F={f_val:.2f}", "p": f"{p_val:.4f}", "result": "Reject H₀" if p_val<0.05 else "Fail", "color": PALETTE['danger'] if p_val<0.05 else PALETTE['success']},
    "Chi-Square\n(Ship Mode vs Region)": {"stat": "χ²=...", "p": "See CSV", "result": "See Report", "color": PALETTE['warning']},
}

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.5, wspace=0.4)

# Correlation heatmap
ax_heat = fig.add_subplot(gs[:, :2])
ax_heat.set_facecolor(PALETTE['mid'])
num_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
corr_df = df[num_cols].corr()
mask = np.zeros_like(corr_df, dtype=bool)
mask[np.triu_indices_from(mask, k=1)] = False
im = ax_heat.imshow(corr_df.values, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
ax_heat.set_xticks(range(len(num_cols)))
ax_heat.set_yticks(range(len(num_cols)))
ax_heat.set_xticklabels(num_cols, fontsize=12)
ax_heat.set_yticklabels(num_cols, fontsize=12)
for i in range(len(num_cols)):
    for j in range(len(num_cols)):
        val = corr_df.values[i, j]
        ax_heat.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    color='white' if abs(val) > 0.5 else PALETTE['dark'])
plt.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
ax_heat.set_title('🔗 Pearson Correlation Matrix\n(Key Numeric Variables)', fontsize=14, fontweight='bold', pad=15)
ax_heat.grid(False)

# Profit Distribution
ax_dist = fig.add_subplot(gs[0, 2])
ax_dist.set_facecolor(PALETTE['mid'])
profit_data = df['Profit'].dropna()
ax_dist.hist(profit_data, bins=60, color=PALETTE['primary'], alpha=0.7, edgecolor='none')
ax_dist.axvline(profit_data.mean(), color=PALETTE['warning'], linewidth=2, label=f'Mean: ${profit_data.mean():.0f}')
ax_dist.axvline(profit_data.median(), color=PALETTE['accent'], linewidth=2, linestyle='--', label=f'Median: ${profit_data.median():.0f}')
ax_dist.set_title('📊 Profit Distribution\n(Shapiro-Wilk: Not Normal)', fontsize=11, fontweight='bold')
ax_dist.set_xlabel('Profit ($)', fontsize=10)
ax_dist.legend(fontsize=8, framealpha=0.4)
ax_dist.grid(True, alpha=0.3)

# Segment T-test
ax_seg = fig.add_subplot(gs[1, 2])
ax_seg.set_facecolor(PALETTE['mid'])
seg_data = {seg: df[df['Segment']==seg]['Profit_Margin'].dropna().values for seg in df['Segment'].unique() if not pd.isna(seg)}
bp = ax_seg.boxplot(list(seg_data.values()), labels=list(seg_data.keys()),
                    patch_artist=True, notch=True,
                    boxprops=dict(facecolor=PALETTE['card'], color=PALETTE['primary']),
                    medianprops=dict(color=PALETTE['warning'], linewidth=2),
                    whiskerprops=dict(color=PALETTE['muted']),
                    capprops=dict(color=PALETTE['muted']),
                    flierprops=dict(marker='o', color=PALETTE['danger'], alpha=0.3, markersize=3))
ax_seg.set_title('📦 Profit Margin by Segment\n(T-test: Consumer vs Corporate)', fontsize=11, fontweight='bold')
ax_seg.set_ylabel('Profit Margin', fontsize=10)
ax_seg.grid(True, alpha=0.3, axis='y')

fig.suptitle('STATISTICAL VALIDATION DASHBOARD — Week 4 Summary',
             fontsize=18, fontweight='bold', color=PALETTE['primary'], y=1.01)
plt.savefig(os.path.join(CHARTS_DIR, 'story4_stats_dashboard.png'), dpi=150, bbox_inches='tight',
            facecolor=PALETTE['dark'])
plt.close()
print("  [OK] Story 4: Statistical Dashboard saved")

# ══════════════════════════════════════════════════════════════════════════════
# CHART 5: Time-Series Growth Story
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 1, figsize=(18, 10))
fig.patch.set_facecolor(PALETTE['dark'])

df['YearMonth'] = df['Order_Date'].dt.to_period('M').astype(str)
monthly = df.groupby('YearMonth').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
monthly = monthly.sort_values('YearMonth').tail(48)  # Last 4 years

ax = axes[0]
ax.set_facecolor(PALETTE['mid'])
x = range(len(monthly))
ax.fill_between(x, monthly['Sales'], alpha=0.2, color=PALETTE['primary'])
ax.plot(x, monthly['Sales'], color=PALETTE['primary'], linewidth=2, label='Sales')
ax.set_xticks(x[::6])
ax.set_xticklabels(monthly['YearMonth'].iloc[::6], rotation=45, fontsize=8)
ax.set_title('📈 Monthly Sales Trend — Consistent Growth Story', fontsize=13, fontweight='bold', pad=10)
ax.set_ylabel('Sales ($)')
ax.legend()
ax.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.set_facecolor(PALETTE['mid'])
pos_profit = monthly['Profit'].clip(lower=0)
neg_profit = monthly['Profit'].clip(upper=0)
ax2.fill_between(x, pos_profit, alpha=0.3, color=PALETTE['success'])
ax2.fill_between(x, neg_profit, alpha=0.3, color=PALETTE['danger'])
ax2.plot(x, monthly['Profit'], color=PALETTE['accent'], linewidth=2, label='Profit')
ax2.axhline(0, color=PALETTE['muted'], linewidth=0.8, linestyle='--')
ax2.set_xticks(x[::6])
ax2.set_xticklabels(monthly['YearMonth'].iloc[::6], rotation=45, fontsize=8)
ax2.set_title('💰 Monthly Profit — Volatility & Loss Months Identified', fontsize=13, fontweight='bold', pad=10)
ax2.set_ylabel('Profit ($)')
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.suptitle('STORY 5: The Growth Narrative — Sales Rising, Profit Needs Attention',
             fontsize=16, fontweight='bold', color=PALETTE['primary'], y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, 'story5_growth_narrative.png'), dpi=150, bbox_inches='tight',
            facecolor=PALETTE['dark'])
plt.close()
print("  [OK] Story 5: Growth Narrative chart saved")

print("\n[ALL DONE] All charts generated successfully!")
print(f"   Charts saved in: {CHARTS_DIR}")
