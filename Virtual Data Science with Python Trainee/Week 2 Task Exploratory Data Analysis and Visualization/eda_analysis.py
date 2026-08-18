"""
Exploratory Data Analysis and Visualization Pipeline
Dataset: Medical Insurance & Health Demographics Dataset
Author: Virtual Data Science with Python Trainee
Week 2 Task: Exploratory Data Analysis and Visualization
"""

import os
import urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configure styling for high-aesthetic visualizations
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#eeeeee'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

PALETTE_PRIMARY = '#1f77b4'
PALETTE_ACCENT = '#ff7f0e'
PALETTE_CUSTOM = ['#2b5c8f', '#e26d5c', '#38b000', '#f4a261', '#9d4edd', '#48cae4']

FIGURES_DIR = os.path.join(os.path.dirname(__file__), 'figures')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)


def load_dataset():
    """Load or download the Medical Insurance Dataset."""
    data_path = os.path.join(DATA_DIR, 'insurance.csv')
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
    
    if not os.path.exists(data_path):
        print(f"Downloading dataset from {url}...")
        urllib.request.urlretrieve(url, data_path)
        print(f"Dataset successfully saved to {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df


def perform_data_audit_and_feature_engineering(df):
    """Clean data and add analytical features for enriched EDA."""
    # Data audit
    print("\n--- DATA AUDIT & OVERVIEW ---")
    print(df.info())
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    
    # Feature Engineering
    # 1. BMI Classification (WHO Guidelines)
    # < 18.5: Underweight, 18.5-24.9: Normal, 25.0-29.9: Overweight, 30.0-34.9: Obese Class I, >= 35: Obese Class II+
    bins = [0, 18.5, 24.9, 29.9, 34.9, 100]
    labels = ['Underweight', 'Normal', 'Overweight', 'Obese Class I', 'Obese Class II+']
    df['bmi_category'] = pd.cut(df['bmi'], bins=bins, labels=labels)
    
    # 2. Age Cohorts
    age_bins = [17, 29, 44, 59, 100]
    age_labels = ['Young Adult (18-29)', 'Early Career (30-44)', 'Mid Career (45-59)', 'Senior (60+)']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)
    
    # 3. Log-transformed Charges for skewness alleviation
    df['log_charges'] = np.log(df['charges'])
    
    # 4. Composite Risk Factor (Smoker & Obese)
    df['is_obese'] = df['bmi'] >= 30.0
    df['is_smoker'] = df['smoker'] == 'yes'
    df['high_risk_segment'] = df.apply(
        lambda row: 'Smoker & Obese' if (row['is_smoker'] and row['is_obese'])
        else ('Smoker Only' if row['is_smoker']
              else ('Obese Non-Smoker' if row['is_obese']
                    else 'Healthy Non-Smoker')),
        axis=1
    )
    
    print("\nFeature Engineering completed successfully.")
    return df


def generate_univariate_visualizations(df):
    """Create comprehensive univariate distribution and frequency charts."""
    print("\nGenerating Univariate Visualizations...")
    
    # 1. Distribution of Target Variable: Medical Charges (Raw vs Log-Transformed)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    
    # Raw Charges
    sns.histplot(df['charges'], kde=True, ax=axes[0], color='#2b5c8f', bins=35, edgecolor='black', alpha=0.65)
    axes[0].axvline(df['charges'].mean(), color='#e63946', linestyle='--', linewidth=2, label=f"Mean: ${df['charges'].mean():,.2f}")
    axes[0].axvline(df['charges'].median(), color='#2a9d8f', linestyle='-', linewidth=2, label=f"Median: ${df['charges'].median():,.2f}")
    axes[0].set_title('Distribution of Medical Charges (Right Skewed)\nSkewness: {:.2f}, Kurtosis: {:.2f}'.format(
        df['charges'].skew(), df['charges'].kurtosis()), fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Medical Charges (USD)', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Frequency (Count)', fontsize=11, fontweight='semibold')
    axes[0].legend(loc='upper right', frameon=True, facecolor='#ffffff', edgecolor='#cccccc')
    
    # Log Charges
    sns.histplot(df['log_charges'], kde=True, ax=axes[1], color='#38b000', bins=30, edgecolor='black', alpha=0.65)
    axes[1].axvline(df['log_charges'].mean(), color='#e63946', linestyle='--', linewidth=2, label=f"Mean: {df['log_charges'].mean():.2f}")
    axes[1].axvline(df['log_charges'].median(), color='#2a9d8f', linestyle='-', linewidth=2, label=f"Median: {df['log_charges'].median():.2f}")
    axes[1].set_title('Log-Transformed Medical Charges Distribution\nSkewness: {:.2f} (Alleviated Skew)'.format(
        df['log_charges'].skew()), fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Log(Medical Charges)', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Frequency (Count)', fontsize=11, fontweight='semibold')
    axes[1].legend(loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#cccccc')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig1_univariate_charges_distribution.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 2. Continuous Demographics: Age and BMI Distributions
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)
    
    # Age Distribution
    sns.histplot(df['age'], kde=True, ax=axes[0], color='#457b9d', bins=25, edgecolor='black', alpha=0.7)
    axes[0].axvline(df['age'].mean(), color='#e63946', linestyle='--', linewidth=2, label=f"Mean Age: {df['age'].mean():.1f} yrs")
    axes[0].set_title('Age Distribution of Policyholders\n(Uniform distribution across adult working lifespan)', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Age (Years)', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Beneficiary Count', fontsize=11, fontweight='semibold')
    axes[0].legend(loc='upper right', frameon=True)
    
    # BMI Distribution
    sns.histplot(df['bmi'], kde=True, ax=axes[1], color='#e76f51', bins=30, edgecolor='black', alpha=0.7)
    axes[1].axvline(30.0, color='#d90429', linestyle='--', linewidth=2, label='Obesity Threshold (BMI = 30)')
    axes[1].axvline(df['bmi'].mean(), color='#2a9d8f', linestyle='-', linewidth=2, label=f"Mean BMI: {df['bmi'].mean():.2f}")
    axes[1].set_title('Body Mass Index (BMI) Distribution\n(Near-Normal with high concentration above Obesity mark)', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Body Mass Index (kg/m²)', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Beneficiary Count', fontsize=11, fontweight='semibold')
    axes[1].legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig2_univariate_age_bmi_distribution.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 3. Categorical Variables Breakdown (Smoking, Region, Sex, Children, BMI Category)
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), dpi=300)
    
    # Smoker Breakdown
    smoker_counts = df['smoker'].value_counts()
    colors_smoker = ['#2a9d8f', '#e63946']
    axes[0, 0].pie(smoker_counts, labels=[f"Non-Smoker ({smoker_counts['no']})", f"Smoker ({smoker_counts['yes']})"], 
                   autopct='%1.1f%%', startangle=140, colors=colors_smoker, explode=(0, 0.08),
                   wedgeprops=dict(edgecolor='white', linewidth=2), textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[0, 0].set_title('Smoking Prevalence in Sample Population', fontsize=13, fontweight='bold', pad=10)
    
    # BMI Categories Countplot
    order_bmi = ['Underweight', 'Normal', 'Overweight', 'Obese Class I', 'Obese Class II+']
    palette_bmi = ['#8ecae6', '#219ebc', '#ffb703', '#fb8500', '#d62828']
    sns.countplot(data=df, x='bmi_category', order=order_bmi, ax=axes[0, 1], palette=palette_bmi, edgecolor='black')
    axes[0, 1].set_title('BMI Categories Classification (WHO Standards)', fontsize=13, fontweight='bold', pad=10)
    axes[0, 1].set_xlabel('BMI Category', fontsize=11, fontweight='semibold')
    axes[0, 1].set_ylabel('Count of Beneficiaries', fontsize=11, fontweight='semibold')
    for p in axes[0, 1].patches:
        axes[0, 1].annotate(f"{int(p.get_height())} ({p.get_height()/len(df)*100:.1f}%)", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=9, fontweight='bold')
    
    # Regional Distribution
    sns.countplot(data=df, x='region', ax=axes[1, 0], palette='crest', edgecolor='black')
    axes[1, 0].set_title('Beneficiary Distribution Across Geographic Regions', fontsize=13, fontweight='bold', pad=10)
    axes[1, 0].set_xlabel('US Region', fontsize=11, fontweight='semibold')
    axes[1, 0].set_ylabel('Count', fontsize=11, fontweight='semibold')
    for p in axes[1, 0].patches:
        axes[1, 0].annotate(f"{int(p.get_height())}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=9, fontweight='bold')
        
    # Children / Dependents Count
    sns.countplot(data=df, x='children', ax=axes[1, 1], palette='flare', edgecolor='black')
    axes[1, 1].set_title('Distribution of Dependent Children Covered', fontsize=13, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel('Number of Children', fontsize=11, fontweight='semibold')
    axes[1, 1].set_ylabel('Count', fontsize=11, fontweight='semibold')
    for p in axes[1, 1].patches:
        axes[1, 1].annotate(f"{int(p.get_height())}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig3_univariate_categorical_distributions.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")


def generate_bivariate_visualizations(df):
    """Create bivariate charts showing interactions between features and medical costs."""
    print("\nGenerating Bivariate Visualizations...")
    
    # 4. Smoking Impact: Violin & Boxplot Comparison
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    
    sns.boxplot(data=df, x='smoker', y='charges', palette=['#2a9d8f', '#e63946'], ax=axes[0], width=0.45, boxprops=dict(alpha=0.85))
    sns.stripplot(data=df, x='smoker', y='charges', color='black', alpha=0.15, jitter=0.2, size=4, ax=axes[0])
    axes[0].set_title('Medical Charges by Smoker Status (Boxplot with Jitter)', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Smoker Status', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Medical Charges (USD)', fontsize=11, fontweight='semibold')
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    
    # Add stats annotations
    mean_no = df[df['smoker'] == 'no']['charges'].mean()
    mean_yes = df[df['smoker'] == 'yes']['charges'].mean()
    axes[0].text(0, mean_no + 2000, f"Mean: ${mean_no:,.0f}", horizontalalignment='center', fontweight='bold', color='#1d3557')
    axes[0].text(1, mean_yes + 2000, f"Mean: ${mean_yes:,.0f}", horizontalalignment='center', fontweight='bold', color='#6a040f')
    
    # Violin Plot for density comparison
    sns.violinplot(data=df, x='smoker', y='charges', palette=['#2a9d8f', '#e63946'], ax=axes[1], inner='quartile', alpha=0.85)
    axes[1].set_title('Density Shape Comparison (Violin Plot)', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Smoker Status', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('Medical Charges (USD)', fontsize=11, fontweight='semibold')
    axes[1].yaxis.set_major_formatter('${x:,.0f}')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig4_bivariate_smoking_impact.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 5. Age vs. Charges with Regression Lines split by Smoker
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    sns.scatterplot(data=df, x='age', y='charges', hue='smoker', palette={'no': '#2a9d8f', 'yes': '#e63946'},
                    alpha=0.7, s=65, edgecolor='w', linewidth=0.5, ax=ax)
    
    # Regression lines
    sns.regplot(data=df[df['smoker'] == 'no'], x='age', y='charges', scatter=False, ax=ax, color='#1d3557', 
                line_kws={'label': 'Non-Smoker Trend (Linear Fit)', 'linewidth': 2.5})
    sns.regplot(data=df[df['smoker'] == 'yes'], x='age', y='charges', scatter=False, ax=ax, color='#9d0208', 
                line_kws={'label': 'Smoker Trend (Linear Fit)', 'linewidth': 2.5})
    
    ax.set_title('Bivariate Relationship: Age vs. Medical Charges Moderated by Smoking Status', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Age of Beneficiary (Years)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Medical Charges (USD)', fontsize=11, fontweight='semibold')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    ax.legend(title='Legend / Trend', frameon=True, facecolor='#ffffff', edgecolor='#cccccc', loc='upper left')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig5_bivariate_age_charges_by_smoker.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 6. BMI vs. Charges with Obesity & Smoker Segmentation
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    
    sns.scatterplot(data=df, x='bmi', y='charges', hue='smoker', style='smoker', 
                    palette={'no': '#2a9d8f', 'yes': '#e63946'}, markers=['o', 'X'], s=75, alpha=0.8, ax=ax)
    
    ax.axvline(30.0, color='#d90429', linestyle='--', linewidth=1.8, label='Clinical Obesity Threshold (BMI = 30)')
    ax.axhline(30000, color='#5c677d', linestyle=':', linewidth=1.5, label='High Expenditure Tier ($30,000)')
    
    ax.text(38, 48000, 'CRITICAL RISK CLUSTER\n(Obese & Smoker: $30k - $60k)', 
            fontsize=10, fontweight='bold', color='#7a040f', bbox=dict(boxstyle='round,pad=0.5', facecolor='#fee2e2', edgecolor='#e63946'))
    
    ax.text(38, 12000, 'Obese Non-Smokers\n(Charges remain < $25k)', 
            fontsize=10, fontweight='bold', color='#1d3557', bbox=dict(boxstyle='round,pad=0.5', facecolor='#e0f2fe', edgecolor='#0284c7'))
    
    ax.set_title('BMI vs. Medical Charges: Non-Linear Interaction with Smoking', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Body Mass Index (BMI)', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Medical Charges (USD)', fontsize=11, fontweight='semibold')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    ax.legend(loc='upper left', frameon=True)
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig6_bivariate_bmi_charges_interaction.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 7. Regional Comparison of Charges and BMI
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)
    
    sns.barplot(data=df, x='region', y='charges', hue='smoker', palette=['#2a9d8f', '#e63946'], ax=axes[0], ci=95, capsize=0.1, edgecolor='black')
    axes[0].set_title('Mean Medical Charges by Region and Smoker Status', fontsize=13, fontweight='bold', pad=12)
    axes[0].set_xlabel('Region', fontsize=11, fontweight='semibold')
    axes[0].set_ylabel('Mean Medical Charges (USD)', fontsize=11, fontweight='semibold')
    axes[0].yaxis.set_major_formatter('${x:,.0f}')
    axes[0].legend(title='Smoker', loc='upper right')
    
    sns.boxplot(data=df, x='region', y='bmi', palette='Set2', ax=axes[1], width=0.5)
    axes[1].axhline(30, color='#e63946', linestyle='--', label='Obesity Line (30)')
    axes[1].set_title('BMI Distribution Across Regions (Southeast exhibits highest median BMI)', fontsize=13, fontweight='bold', pad=12)
    axes[1].set_xlabel('Region', fontsize=11, fontweight='semibold')
    axes[1].set_ylabel('BMI (kg/m²)', fontsize=11, fontweight='semibold')
    axes[1].legend(loc='upper right')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig7_bivariate_regional_analysis.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")


def generate_multivariate_visualizations(df):
    """Create multivariate correlation, facet grids, and composite risk visualizations."""
    print("\nGenerating Multivariate Visualizations...")
    
    # 8. Correlation Matrix (Numerical features + encoded categorical variables)
    df_encoded = df.copy()
    df_encoded['smoker_numeric'] = df_encoded['smoker'].map({'yes': 1, 'no': 0})
    df_encoded['sex_numeric'] = df_encoded['sex'].map({'male': 1, 'female': 0})
    
    corr_cols = ['age', 'bmi', 'children', 'smoker_numeric', 'sex_numeric', 'charges', 'log_charges']
    corr_matrix = df_encoded[corr_cols].corr()
    
    fig, ax = plt.subplots(figsize=(9, 7.5), dpi=300)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', vmin=-0.1, vmax=1.0, 
                cbar_kws={'label': 'Pearson Correlation Coefficient'}, linewidths=1.2, linecolor='white',
                square=True, ax=ax, mask=mask)
    
    ax.set_title('Multivariate Correlation Heatmap (Health & Cost Determinants)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticklabels(['Age', 'BMI', 'Children', 'Smoker', 'Sex (Male)', 'Charges ($)', 'Log(Charges)'], rotation=30, ha='right', fontweight='semibold')
    ax.set_yticklabels(['Age', 'BMI', 'Children', 'Smoker', 'Sex (Male)', 'Charges ($)', 'Log(Charges)'], rotation=0, fontweight='semibold')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig8_multivariate_correlation_heatmap.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 9. Facet Grid: Age vs Charges across BMI Categories, stratified by Smoking Status
    g = sns.FacetGrid(df, col='bmi_category', hue='smoker', palette={'no': '#2a9d8f', 'yes': '#e63946'}, 
                      col_wrap=3, height=4, aspect=1.1, sharey=True)
    g.map(sns.scatterplot, 'age', 'charges', alpha=0.75, s=55, edgecolor='black', linewidth=0.3)
    g.add_legend(title='Smoker Status', loc='upper right')
    g.set_axis_labels('Age (Years)', 'Medical Charges ($)')
    g.fig.subplots_adjust(top=0.88)
    g.fig.suptitle('Multivariate Facet Grid: Age vs. Charges by BMI Category & Smoking Behavior', fontsize=14, fontweight='bold')
    
    fig_path = os.path.join(FIGURES_DIR, 'fig9_multivariate_facetgrid_bmi_age_smoker.png')
    g.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 10. Composite Risk Segment Analysis
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    
    order_risk = ['Healthy Non-Smoker', 'Obese Non-Smoker', 'Smoker Only', 'Smoker & Obese']
    palette_risk = ['#2a9d8f', '#457b9d', '#f4a261', '#e63946']
    
    sns.boxplot(data=df, x='high_risk_segment', y='charges', order=order_risk, palette=palette_risk, ax=ax, width=0.5)
    
    # Add mean labels
    means = df.groupby('high_risk_segment')['charges'].mean().reindex(order_risk)
    for i, (seg, mean_val) in enumerate(means.items()):
        ax.text(i, mean_val + 2000, f"Mean: ${mean_val:,.0f}", horizontalalignment='center', fontweight='bold', color='#1d3557', fontsize=9.5)
        
    ax.set_title('Composite Risk Segmentation vs. Annual Medical Incurred Costs', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Patient Risk Segment Profile', fontsize=11, fontweight='semibold')
    ax.set_ylabel('Annual Charges (USD)', fontsize=11, fontweight='semibold')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    
    plt.tight_layout()
    fig_path = os.path.join(FIGURES_DIR, 'fig10_multivariate_risk_segmentation.png')
    plt.savefig(fig_path)
    plt.close()
    print(f"Saved: {fig_path}")
    
    # 11. Pairplot of Continuous Features stratified by Smoker
    pairplot_cols = ['age', 'bmi', 'charges']
    pp = sns.pairplot(df[pairplot_cols + ['smoker']], hue='smoker', palette={'no': '#2a9d8f', 'yes': '#e63946'}, 
                      diag_kind='kde', plot_kws={'alpha': 0.6, 's': 40, 'edgecolor': 'none'}, height=2.8)
    pp.fig.subplots_adjust(top=0.93)
    pp.fig.suptitle('Pairwise Feature Interactions Stratified by Smoker Status', fontsize=13, fontweight='bold')
    
    fig_path = os.path.join(FIGURES_DIR, 'fig11_multivariate_pairplot.png')
    pp.savefig(fig_path, dpi=300)
    plt.close()
    print(f"Saved: {fig_path}")


def compute_statistical_aggregations(df):
    """Compute and print statistical aggregates and pivot tables."""
    print("\n--- STATISTICAL AGGREGATIONS & SUMMARY TABLES ---")
    
    # 1. Overall Descriptive Statistics
    desc_stats = df[['age', 'bmi', 'children', 'charges', 'log_charges']].describe().T
    desc_stats['skewness'] = [df['age'].skew(), df['bmi'].skew(), df['children'].skew(), df['charges'].skew(), df['log_charges'].skew()]
    desc_stats['kurtosis'] = [df['age'].kurtosis(), df['bmi'].kurtosis(), df['children'].kurtosis(), df['charges'].kurtosis(), df['log_charges'].kurtosis()]
    print("\nOverall Summary Table:\n", desc_stats.round(2))
    
    # 2. Charges by Smoker Status
    smoker_agg = df.groupby('smoker')['charges'].agg(['count', 'mean', 'median', 'std', lambda x: np.percentile(x, 75) - np.percentile(x, 25)]).rename(columns={'<lambda_0>': 'IQR'})
    print("\nCharges by Smoker:\n", smoker_agg.round(2))
    
    # 3. Pivot Table: Smoker x BMI Category
    pivot_smoker_bmi = df.pivot_table(index='bmi_category', columns='smoker', values='charges', aggfunc=['mean', 'median', 'count'])
    print("\nPivot Table (BMI Category vs Smoker):\n", pivot_smoker_bmi.round(2))
    
    # 4. Regional Breakdown
    regional_agg = df.groupby('region').agg(
        total_count=('charges', 'count'),
        mean_charges=('charges', 'mean'),
        median_charges=('charges', 'median'),
        mean_bmi=('bmi', 'mean'),
        smoker_rate=('is_smoker', 'mean')
    )
    print("\nRegional Summary:\n", regional_agg.round(2))
    
    # 5. Risk Segment Breakdown
    risk_agg = df.groupby('high_risk_segment').agg(
        count=('charges', 'count'),
        mean_charges=('charges', 'mean'),
        median_charges=('charges', 'median'),
        pct_of_total_costs=('charges', lambda x: x.sum() / df['charges'].sum() * 100)
    ).reindex(['Healthy Non-Smoker', 'Obese Non-Smoker', 'Smoker Only', 'Smoker & Obese'])
    print("\nRisk Segment Summary:\n", risk_agg.round(2))
    
    return {
        'desc_stats': desc_stats,
        'smoker_agg': smoker_agg,
        'pivot_smoker_bmi': pivot_smoker_bmi,
        'regional_agg': regional_agg,
        'risk_agg': risk_agg
    }


def main():
    print("=================================================================")
    print("  STARTING WEEK 2 EXPLORATORY DATA ANALYSIS (EDA) PIPELINE       ")
    print("=================================================================")
    df = load_dataset()
    df = perform_data_audit_and_feature_engineering(df)
    
    generate_univariate_visualizations(df)
    generate_bivariate_visualizations(df)
    generate_multivariate_visualizations(df)
    
    stats_dict = compute_statistical_aggregations(df)
    print("\nAll visualizations and statistical analyses completed successfully!")


if __name__ == '__main__':
    main()
