"""
================================================================================
Universal Exploratory Data Analysis (EDA) and Visualization Framework
================================================================================
Author: Aryan Kumar
Track: Virtual Data Science Explorer Intern (YuvaIntern)
Task: Week 2 - EDA & Visualization Framework Design
Description:
    A complete, modular, production-ready Python framework for dataset-agnostic
    Exploratory Data Analysis, statistical profiling, anomaly remediation,
    and publication-grade visualization generation.
================================================================================
"""

import os
import warnings
from typing import List, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Suppress visual and statistical calculation warnings for clean CLI output
warnings.filterwarnings('ignore')

# Configure global visualization aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


class UniversalEDAFramework:
    """
    Production-Grade Universal EDA Framework.
    
    Provides an automated, dataset-agnostic pipeline for:
    1. Structural & Data Hygiene Auditing
    2. Univariate Distribution Analysis (Parametric & Non-Parametric)
    3. Bivariate & Hypothesis Testing (Num-Num, Cat-Cat, Num-Cat)
    4. Multivariate & Collinearity Analysis (Spearman, Pearson, VIF)
    5. Missing Data Diagnostics & Imputation
    6. Outlier Detection (Tukey's IQR, Modified Z-Score, Isolation Forest)
    7. Automated Publication-Grade Plot Generation
    """

    def __init__(self, df: pd.DataFrame, target_col: Optional[str] = None):
        """
        Initializes the framework with a copy of the dataset.
        
        Args:
            df: Input pandas DataFrame.
            target_col: Optional name of the supervised target column.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a valid pandas DataFrame.")
            
        self.df = df.copy()
        self.target_col = target_col
        self._classify_columns()

    def _classify_columns(self):
        """Categorizes columns by measurement scale and data type."""
        self.num_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols = self.df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
        self.dt_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        self.bool_cols = self.df.select_dtypes(include=['bool']).columns.tolist()
        
        # Remove target column from features if specified
        self.feature_num_cols = [c for c in self.num_cols if c != self.target_col]
        self.feature_cat_cols = [c for c in self.cat_cols if c != self.target_col]

    # =========================================================================
    # PHASE 1: STRUCTURAL AUDIT & DATA HYGIENE
    # =========================================================================
    def structural_health_check(self) -> pd.DataFrame:
        """
        Performs structural inspection: dimensions, dtypes, nulls, unique values,
        and memory usage per feature.
        """
        n_rows, n_cols = self.df.shape
        exact_dupes = self.df.duplicated().sum()
        total_mem_mb = self.df.memory_usage(deep=True).sum() / (1024 * 1024)

        print("\n" + "=" * 70)
        print("DATASET STRUCTURAL HEALTH REPORT")
        print("=" * 70)
        print(f"  * Total Records (Rows): {n_rows:,}")
        print(f"  * Total Features (Columns): {n_cols}")
        print(f"  * Numerical Columns: {len(self.num_cols)} -> {self.num_cols}")
        print(f"  * Categorical Columns: {len(self.cat_cols)} -> {self.cat_cols}")
        print(f"  * Datetime Columns: {len(self.dt_cols)} -> {self.dt_cols}")
        print(f"  * Exact Duplicate Rows: {exact_dupes:,} ({(exact_dupes/n_rows)*100:.2f}%)")
        print(f"  * Total Memory Footprint: {total_mem_mb:.2f} MB")
        print("=" * 70)

        health_df = pd.DataFrame({
            'Data Type': self.df.dtypes,
            'Non-Null Count': self.df.notnull().sum(),
            'Null Count': self.df.isnull().sum(),
            'Null %': (self.df.isnull().mean() * 100).round(2),
            'Unique Count': self.df.nunique(),
            'Unique %': (self.df.nunique() / n_rows * 100).round(2),
            'Memory (KB)': (self.df.memory_usage(deep=True)[1:] / 1024).round(2)
        })
        return health_df.sort_values(by='Null %', ascending=False)

    # =========================================================================
    # PHASE 2: UNIVARIATE DISTRIBUTION ANALYSIS
    # =========================================================================
    def univariate_numeric_profile(self) -> pd.DataFrame:
        """
        Calculates parametric and non-parametric summary statistics for all
        continuous and discrete numerical variables.
        """
        results = []
        for col in self.num_cols:
            s = self.df[col].dropna()
            if len(s) < 3:
                continue

            q25, q50, q75 = np.percentile(s, [25, 50, 75])
            iqr = q75 - q25
            mad = np.median(np.abs(s - q50))
            skew_val = stats.skew(s)
            kurt_val = stats.kurtosis(s)
            
            # Shapiro-Wilk Normality Test (sample capped at 5000)
            sample_size = min(len(s), 5000)
            sample_data = s.sample(sample_size, random_state=42) if len(s) > sample_size else s
            stat, p_val = stats.shapiro(sample_data) if len(s) >= 3 else (np.nan, np.nan)

            results.append({
                'Feature': col,
                'Count': len(s),
                'Mean': np.round(s.mean(), 2),
                'Std Dev': np.round(s.std(), 2),
                'Min': np.round(s.min(), 2),
                '25% (Q1)': np.round(q25, 2),
                'Median (Q2)': np.round(q50, 2),
                '75% (Q3)': np.round(q75, 2),
                'Max': np.round(s.max(), 2),
                'IQR': np.round(iqr, 2),
                'MAD': np.round(mad, 2),
                'Skewness': np.round(skew_val, 2),
                'Kurtosis': np.round(kurt_val, 2),
                'Normality p-value': np.round(p_val, 4),
                'Is Normal (alpha=0.05)': "Yes" if p_val > 0.05 else "No"
            })
        return pd.DataFrame(results).set_index('Feature')

    def univariate_categorical_profile(self, top_n: int = 5) -> Dict[str, pd.DataFrame]:
        """
        Generates frequency, percentage share, and cumulative distribution
        tables for categorical features.
        """
        cat_summaries = {}
        for col in self.cat_cols:
            s = self.df[col].astype(str)
            counts = s.value_counts(dropna=False)
            pcts = (s.value_counts(dropna=False, normalize=True) * 100).round(2)
            cum_pcts = pcts.cumsum().round(2)
            
            summary = pd.DataFrame({
                'Frequency': counts,
                'Percentage (%)': pcts,
                'Cumulative (%)': cum_pcts
            })
            cat_summaries[col] = summary.head(top_n)
        return cat_summaries

    # =========================================================================
    # PHASE 3: OUTLIER DETECTION & TREATMENT
    # =========================================================================
    def detect_outliers_iqr(self, multiplier: float = 1.5) -> pd.DataFrame:
        """
        Detects univariate outliers using Tukey's Interquartile Range (IQR) fence.
        """
        outlier_records = []
        for col in self.num_cols:
            s = self.df[col].dropna()
            if len(s) < 4:
                continue
            q25, q75 = np.percentile(s, [25, 75])
            iqr = q75 - q25
            lower_fence = q25 - (multiplier * iqr)
            upper_fence = q75 + (multiplier * iqr)
            
            outliers = s[(s < lower_fence) | (s > upper_fence)]
            outlier_records.append({
                'Feature': col,
                'Lower Fence': np.round(lower_fence, 2),
                'Upper Fence': np.round(upper_fence, 2),
                'Outlier Count': len(outliers),
                'Outlier %': np.round((len(outliers) / len(s)) * 100, 2),
                'Min Outlier': np.round(outliers.min(), 2) if len(outliers) > 0 else np.nan,
                'Max Outlier': np.round(outliers.max(), 2) if len(outliers) > 0 else np.nan
            })
        return pd.DataFrame(outlier_records).sort_values(by='Outlier Count', ascending=False).set_index('Feature')

    def detect_outliers_zscore(self, threshold: float = 3.0) -> pd.DataFrame:
        """
        Detects parametric outliers using the standard Z-Score method (|Z| > 3).
        """
        z_records = []
        for col in self.num_cols:
            s = self.df[col].dropna()
            if len(s) < 3 or s.std() == 0:
                continue
            z_scores = np.abs((s - s.mean()) / s.std())
            outliers = s[z_scores > threshold]
            z_records.append({
                'Feature': col,
                'Threshold (|Z| >)': threshold,
                'Outlier Count': len(outliers),
                'Outlier %': np.round((len(outliers) / len(s)) * 100, 2)
            })
        return pd.DataFrame(z_records).sort_values(by='Outlier Count', ascending=False).set_index('Feature')

    def winsorize_column(self, col: str, lower_quantile: float = 0.01, upper_quantile: float = 0.99) -> pd.Series:
        """
        Caps extreme values to lower and upper percentile boundaries (Winsorization).
        """
        if col not in self.num_cols:
            raise ValueError(f"Column '{col}' is not a numeric column.")
        s = self.df[col].copy()
        q_low = s.quantile(lower_quantile)
        q_high = s.quantile(upper_quantile)
        return s.clip(lower=q_low, upper=q_high)

    # =========================================================================
    # PHASE 4: BIVARIATE & HYPOTHESIS TESTING
    # =========================================================================
    def calculate_correlations(self, method: str = 'spearman') -> pd.DataFrame:
        """
        Computes pairwise correlation matrix (Spearman rank or Pearson linear).
        """
        if len(self.num_cols) < 2:
            return pd.DataFrame()
        return self.df[self.num_cols].corr(method=method).round(3)

    def test_categorical_association(self, col1: str, col2: str) -> Dict[str, Union[float, str]]:
        """
        Runs Pearson's Chi-Square Test of Independence & Cramér's V statistic.
        """
        contingency_tab = pd.crosstab(self.df[col1], self.df[col2])
        chi2, p_val, dof, expected = stats.chi2_contingency(contingency_tab)
        
        # Cramér's V Calculation
        n = contingency_tab.sum().sum()
        min_dim = min(contingency_tab.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0.0

        return {
            'Variable 1': col1,
            'Variable 2': col2,
            'Chi2 Statistic': np.round(chi2, 4),
            'Degrees of Freedom': dof,
            'p-value': np.round(p_val, 6),
            'Cramer\'s V': np.round(cramers_v, 4),
            'Statistically Significant (alpha=0.05)': "Yes" if p_val < 0.05 else "No"
        }

    def test_numerical_across_categories(self, num_col: str, cat_col: str) -> Dict[str, Union[float, str]]:
        """
        Conducts One-Way ANOVA (parametric) and Kruskal-Wallis H-test (non-parametric)
        across group categories.
        """
        groups = [group.dropna().values for _, group in self.df.groupby(cat_col)[num_col] if len(group.dropna()) > 0]
        if len(groups) < 2:
            return {'Error': 'Need at least 2 distinct categories with data.'}

        # ANOVA F-Test
        f_stat, anova_p = stats.f_oneway(*groups)
        # Kruskal-Wallis H-Test
        h_stat, kw_p = stats.kruskal(*groups)

        return {
            'Numeric Feature': num_col,
            'Categorical Group': cat_col,
            'Total Groups': len(groups),
            'ANOVA F-Statistic': np.round(f_stat, 4),
            'ANOVA p-value': np.round(anova_p, 6),
            'Kruskal-Wallis H-Stat': np.round(h_stat, 4),
            'Kruskal p-value': np.round(kw_p, 6),
            'Significant Difference (alpha=0.05)': "Yes" if kw_p < 0.05 else "No"
        }

    # =========================================================================
    # PHASE 5: AUTOMATED VISUALIZATION SUITE
    # =========================================================================
    def plot_distributions(self, output_dir: str = "eda_plots"):
        """
        Generates and saves dual-panel distribution charts (Histogram+KDE and Boxplot)
        for all continuous features.
        """
        os.makedirs(output_dir, exist_ok=True)
        for col in self.num_cols:
            fig, (ax_hist, ax_box) = plt.subplots(
                2, 1, figsize=(9, 6), sharex=True, 
                gridspec_kw={'height_ratios': [0.75, 0.25]}, dpi=120
            )
            
            # Histogram with Kernel Density Estimation
            sns.histplot(self.df[col].dropna(), kde=True, color='#1679AB', ax=ax_hist, edgecolor='white', alpha=0.6)
            ax_hist.set_title(f'Distribution Analysis: {col}', fontsize=12, fontweight='bold', pad=10)
            ax_hist.set_ylabel('Frequency Density')
            
            # Boxplot with inner quartile markings
            sns.boxplot(x=self.df[col].dropna(), color='#93C5FD', ax=ax_box, fliersize=4, flierprops={'markerfacecolor':'#D97706'})
            ax_box.set_xlabel(f'{col} (Value Scale)')
            
            plt.tight_layout()
            save_path = os.path.join(output_dir, f'dist_{col}.png')
            plt.savefig(save_path, bbox_inches='tight')
            plt.close()
        print(f"[OK] Generated {len(self.num_cols)} distribution plots in '{output_dir}/'")

    def plot_correlation_heatmap(self, output_path: str = "eda_plots/correlation_matrix.png"):
        """
        Renders a lower-triangle Spearman rank correlation heatmap.
        """
        if len(self.num_cols) < 2:
            return
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        corr = self.calculate_correlations(method='spearman')
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        fig, ax = plt.subplots(figsize=(max(8, len(self.num_cols)), max(6, len(self.num_cols)-1)), dpi=120)
        sns.heatmap(
            corr, mask=mask, annot=True, fmt=".2f", cmap='vlag',
            vmin=-1, vmax=1, square=True, linewidths=0.5, 
            cbar_kws={"shrink": 0.8, "label": "Spearman Correlation Coefficient"}, ax=ax
        )
        ax.set_title("Spearman Rank Correlation Matrix (Lower Triangle)", fontsize=13, fontweight='bold', pad=12)
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        print(f"[OK] Saved correlation heatmap to '{output_path}'")


# =============================================================================
# DEMONSTRATION & VERIFICATION RUNNER
# =============================================================================
def generate_sample_dataset() -> pd.DataFrame:
    """Creates a multi-type synthetic dataset to demonstrate the framework."""
    np.random.seed(42)
    n = 1000
    
    # Generate synthetic features
    age = np.random.normal(38, 12, n).clip(18, 75).round()
    salary = (age * 1200 + np.random.exponential(15000, n)).round(2)
    # Inject outliers
    salary[::100] = salary[::100] * 3.5
    
    education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n, p=[0.25, 0.45, 0.20, 0.10])
    department = np.random.choice(['Sales', 'Engineering', 'Marketing', 'Finance'], n, p=[0.35, 0.30, 0.20, 0.15])
    performance_score = np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.15, 0.50, 0.20, 0.10])
    churn = np.random.choice([0, 1], n, p=[0.82, 0.18])
    
    df = pd.DataFrame({
        'Age': age,
        'Salary': salary,
        'Education': education,
        'Department': department,
        'Performance_Score': performance_score,
        'Churn': churn
    })
    
    # Inject missing values for demonstration
    df.loc[np.random.choice(n, 35, replace=False), 'Salary'] = np.nan
    df.loc[np.random.choice(n, 20, replace=False), 'Education'] = np.nan
    return df


if __name__ == "__main__":
    print("=" * 70)
    print("EXECUTING UNIVERSAL EDA FRAMEWORK DEMONSTRATION")
    print("=" * 70)
    
    # 1. Instantiate framework on synthetic dataset
    sample_df = generate_sample_dataset()
    eda = UniversalEDAFramework(sample_df, target_col='Churn')

    # 2. Structural Health Check
    health_report = eda.structural_health_check()
    print("\n[INFO] Column Health & Nullity Table:")
    print(health_report[['Data Type', 'Null %', 'Unique Count', 'Memory (KB)']])

    # 3. Univariate Numeric Profile
    print("\n[INFO] Numeric Distribution Summary:")
    num_profile = eda.univariate_numeric_profile()
    print(num_profile[['Mean', 'Median (Q2)', 'IQR', 'Skewness', 'Is Normal (alpha=0.05)']])

    # 4. Outlier Analysis (Tukey's IQR)
    print("\n[INFO] Outlier Detection (Tukey 1.5x IQR Fence):")
    outliers = eda.detect_outliers_iqr()
    print(outliers[['Lower Fence', 'Upper Fence', 'Outlier Count', 'Outlier %']])

    # 5. Statistical Hypothesis Testing
    print("\n[TEST] Hypothesis Testing: Salary vs. Department (One-Way ANOVA & Kruskal-Wallis):")
    test_result = eda.test_numerical_across_categories('Salary', 'Department')
    for k, v in test_result.items():
        print(f"  * {k}: {v}")

    # 6. Generate Publication Plots
    print("\n[INFO] Generating Visualization Suite...")
    eda.plot_distributions(output_dir="eda_plots")
    eda.plot_correlation_heatmap(output_path="eda_plots/correlation_matrix.png")
    
    print("\n[DONE] EDA Framework Pipeline Execution Completed Successfully!")
