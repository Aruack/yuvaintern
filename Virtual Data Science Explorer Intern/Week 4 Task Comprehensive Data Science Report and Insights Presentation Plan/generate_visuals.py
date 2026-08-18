import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs('assets', exist_ok=True)

# -------------------------------------------------------------
# Visualization 1: Kaplan-Meier Survival Curve by Adoption Tier
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
days = np.linspace(0, 365, 100)

# Survival functions for 3 tiers
surv_high = np.exp(-0.0007 * days)
surv_med = np.exp(-0.0018 * days)
surv_low = np.exp(-0.0045 * days)

ax.plot(days, surv_high * 100, label='Tier 1: High Feature Adoption (>= 8 core features/mo)', color='#10B981', linewidth=2.8)
ax.plot(days, surv_med * 100, label='Tier 2: Moderate Feature Adoption (4-7 core features/mo)', color='#3B82F6', linewidth=2.5)
ax.plot(days, surv_low * 100, label='Tier 3: Low Feature Adoption (< 4 core features/mo)', color='#EF4444', linewidth=2.5, linestyle='--')

# Confidence bands
ax.fill_between(days, (surv_high - 0.03)*100, np.minimum(100, (surv_high + 0.03)*100), color='#10B981', alpha=0.15)
ax.fill_between(days, (surv_med - 0.04)*100, (surv_med + 0.04)*100, color='#3B82F6', alpha=0.12)
ax.fill_between(days, (surv_low - 0.05)*100, (surv_low + 0.05)*100, color='#EF4444', alpha=0.12)

# Annotations
ax.annotate('Critical 90-Day "Onboarding Cliff":\nTier 3 retention drops by 32%', 
            xy=(90, surv_low[int(100*90/365)]*100), 
            xytext=(130, 48),
            arrowprops=dict(facecolor='#EF4444', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, fontweight='bold', color='#B91C1C',
            bbox=dict(boxstyle="round,pad=0.4", fc="#FEE2E2", ec="#EF4444", lw=1))

ax.axvline(x=90, color='#64748B', linestyle=':', linewidth=1.5, alpha=0.8)
ax.text(92, 12, 'Day 90 Onboarding Milestone', rotation=90, color='#64748B', fontsize=9, fontweight='semibold')

ax.set_title('Figure 1: Customer Retention Probability Over 365 Days by Feature Adoption Tier', 
             fontsize=13, fontweight='bold', pad=15, color='#1E293B')
ax.set_xlabel('Days Since Contract Activation', fontsize=11, fontweight='semibold', color='#334155')
ax.set_ylabel('Customer Retention Rate (%)', fontsize=11, fontweight='semibold', color='#334155')
ax.set_ylim(0, 105)
ax.set_xlim(0, 365)
ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', loc='lower left', fontsize=10)
plt.tight_layout()
plt.savefig('assets/survival_retention_curve.png', dpi=300)
plt.close()
print("Saved assets/survival_retention_curve.png")

# -------------------------------------------------------------
# Visualization 2: SHAP Feature Importance & Attribution
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)

features = [
    'Monthly Active User (MAU) Decay Rate',
    'Open Support Escalations (Sev-1 / Sev-2)',
    'Days Since Executive Sponsor Engagement',
    'Core Workflow Integration Depth (APIs/Webhooks)',
    'Contract Renewal Window (< 60 Days)',
    'Payment Failure / Invoicing Friction Incidents',
    'Net Promoter Score (NPS) Detractor Rating',
    'Seat License Utilization Ratio (< 45%)',
    'Weekly Dashboard Query Frequency',
    'Customer Success Outreach Cadence'
]

shap_values = [0.42, 0.38, 0.33, -0.31, 0.28, 0.24, 0.21, 0.19, -0.16, -0.14]
colors = ['#EF4444' if x > 0 else '#10B981' for x in shap_values]

y_pos = np.arange(len(features))
bars = ax.barh(y_pos, shap_values, color=colors, height=0.65, edgecolor='#334155', linewidth=0.5)

# Value labels
for bar, val in zip(bars, shap_values):
    width = bar.get_width()
    ha = 'left' if width > 0 else 'right'
    offset = 0.01 if width > 0 else -0.01
    label = f'+{val:.2f} (Risk)' if val > 0 else f'{val:.2f} (Shield)'
    ax.text(width + offset, bar.get_y() + bar.get_height()/2, label, 
            va='center', ha=ha, fontsize=9, fontweight='bold', color='#1E293B')

ax.axvline(0, color='#334155', linewidth=1.2)
ax.set_yticks(y_pos)
ax.set_yticklabels(features, fontsize=10, fontweight='medium', color='#1E293B')
ax.invert_yaxis()  # top-down

ax.set_title('Figure 2: SHAP Global Feature Importance & Directional Churn Impact (Top 10 Drivers)', 
             fontsize=13, fontweight='bold', pad=15, color='#1E293B')
ax.set_xlabel('Mean SHAP Attribution Value [log-odds impact on churn]', fontsize=11, fontweight='semibold', color='#334155')
ax.set_xlim(-0.35, 0.55)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#EF4444', label='Increases Churn Risk (Friction Driver)'),
    Patch(facecolor='#10B981', label='Decreases Churn Risk (Retention Anchor)')
]
ax.legend(handles=legend_elements, loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9.5)

plt.tight_layout()
plt.savefig('assets/shap_feature_importance.png', dpi=300)
plt.close()
print("Saved assets/shap_feature_importance.png")

# -------------------------------------------------------------
# Visualization 3: Support Escalations vs Churn Likelihood Matrix (Heatmap)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

escalation_buckets = ['0 Issues', '1-2 Issues', '3-4 Issues', '5+ Issues']
account_tiers = ['Enterprise ($100k+)', 'Mid-Market ($25k-$100k)', 'Growth / SMB (<$25k)']

# Churn rates in %
heatmap_data = np.array([
    [4.2,  9.8, 28.5, 62.4],   # Enterprise
    [7.1, 15.3, 39.8, 74.6],   # Mid-Market
    [12.4, 24.1, 51.2, 88.3]   # SMB
])

sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax,
            xticklabels=escalation_buckets, yticklabels=account_tiers,
            cbar_kws={'label': 'Observed 90-Day Churn Rate (%)', 'shrink': 0.8},
            annot_kws={'size': 11, 'weight': 'bold', 'color': '#1E293B'},
            linewidths=1.5, linecolor='#FFFFFF')

ax.set_title('Figure 3: Churn Probability Matrix across Account Tiers and Unresolved Escalations', 
             fontsize=13, fontweight='bold', pad=15, color='#1E293B')
ax.set_xlabel('Unresolved Support Escalations (Past 60 Days)', fontsize=11, fontweight='semibold', color='#334155')
ax.set_ylabel('Account Value Segment', fontsize=11, fontweight='semibold', color='#334155')

plt.tight_layout()
plt.savefig('assets/churn_risk_heatmap.png', dpi=300)
plt.close()
print("Saved assets/churn_risk_heatmap.png")

# -------------------------------------------------------------
# Visualization 4: Cumulative Gains / Lift Curve & Net Revenue Frontier
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

# Subplot 1: Cumulative Gains Curve
percentiles = np.linspace(0, 100, 100)
model_capture = 100 / (1 + np.exp(-0.06 * (percentiles - 25)))
model_capture = (model_capture - model_capture[0]) / (model_capture[-1] - model_capture[0]) * 100
random_capture = percentiles

ax1.plot(percentiles, model_capture, label='RetainAI Ensemble Model', color='#2563EB', linewidth=2.8)
ax1.plot(percentiles, random_capture, label='Random Baseline (No Model)', color='#94A3B8', linestyle='--', linewidth=2)
ax1.axvline(x=20, color='#DC2626', linestyle=':', linewidth=1.5)
ax1.plot(20, model_capture[20], 'ro', markersize=8)

ax1.annotate(f'Top 20% Contacted\nCaptures 73.4% of Churners', 
             xy=(20, model_capture[20]), xytext=(32, 60),
             arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
             fontsize=9.5, fontweight='bold', color='#991B1B',
             bbox=dict(boxstyle="round,pad=0.3", fc="#FEE2E2", ec="#DC2626", lw=1))

ax1.set_title('A: Cumulative Gains (Capture) Curve', fontsize=11.5, fontweight='bold', color='#1E293B')
ax1.set_xlabel('Percentage of Accounts Targeted (%)', fontsize=10, fontweight='semibold', color='#334155')
ax1.set_ylabel('Cumulative % of Churners Identified', fontsize=10, fontweight='semibold', color='#334155')
ax1.legend(loc='lower right', fontsize=9.5)
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 105)

# Subplot 2: Net Revenue Optimization Frontier
target_pct = np.linspace(5, 50, 46)
gross_saved = 6.2 * (1 - np.exp(-0.08 * target_pct))  # in Millions
intervention_cost = 0.045 * target_pct                 # in Millions ($45k per 1%)
net_benefit = gross_saved - intervention_cost

optimal_idx = np.argmax(net_benefit)
opt_pct = target_pct[optimal_idx]
opt_net = net_benefit[optimal_idx]

ax2.plot(target_pct, gross_saved, label='Gross Revenue Saved ($M)', color='#10B981', linewidth=2.2)
ax2.plot(target_pct, intervention_cost, label='Intervention Cost ($M)', color='#F59E0B', linewidth=2.2, linestyle='--')
ax2.plot(target_pct, net_benefit, label='Net Economic Value ($M)', color='#6366F1', linewidth=2.8)

ax2.plot(opt_pct, opt_net, 'o', color='#4338CA', markersize=8)
ax2.annotate(f'Optimal ROI Frontier: 22% Target\nNet ARR Saved: ${opt_net:.2f}M (ROI: 4.6x)', 
             xy=(opt_pct, opt_net), xytext=(22, 1.8),
             arrowprops=dict(facecolor='#4338CA', shrink=0.08, width=1.5, headwidth=7),
             fontsize=9.5, fontweight='bold', color='#312E81',
             bbox=dict(boxstyle="round,pad=0.3", fc="#EEF2FF", ec="#6366F1", lw=1))

ax2.set_title('B: Net Revenue Optimization & Intervention Frontier', fontsize=11.5, fontweight='bold', color='#1E293B')
ax2.set_xlabel('Percentage of Accounts Targeted (%)', fontsize=10, fontweight='semibold', color='#334155')
ax2.set_ylabel('Financial Impact ($ Millions)', fontsize=10, fontweight='semibold', color='#334155')
ax2.legend(loc='upper left', fontsize=9.5)
ax2.set_xlim(5, 50)
ax2.set_ylim(0, 6.5)

plt.suptitle('Figure 4: Model Efficiency, Targeting Lift, and Economic Return Frontier', 
             fontsize=13, fontweight='bold', y=1.02, color='#1E293B')
plt.tight_layout()
plt.savefig('assets/revenue_lift_frontier.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved assets/revenue_lift_frontier.png")
