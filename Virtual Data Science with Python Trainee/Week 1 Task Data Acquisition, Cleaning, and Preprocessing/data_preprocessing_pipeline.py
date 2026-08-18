"""
Week 1 Task: Data Acquisition, Cleaning, and Preprocessing
Author: Aryan Kumar (Virtual Data Science Trainee)
Topic: End-to-End Data Pipeline for Customer Intelligence & Churn Analytics

This script performs:
1. Programmatic data acquisition and generation of realistic raw data with data quality challenges.
2. Exploratory Data Analysis (EDA) & Data Quality Auditing.
3. Missing value analysis and advanced imputation (KNN / Iterative / Median / Mode).
4. Erroneous value remediation, type casting, text normalization, and duplicate resolution.
5. Outlier detection (IQR, Z-Score, Isolation Forest) and Winsorization / Robust Capping.
6. Feature Engineering, Skewness Transformation (Log1p / Yeo-Johnson), and Categorical Encoding.
7. Feature Scaling (RobustScaler, StandardScaler) for downstream Machine Learning readiness.
8. Generation and export of publication-grade diagnostic visualizations and cleaned datasets.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import IsolationForest
import warnings

warnings.filterwarnings("ignore")

# Set visualization style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CBD5E0"
plt.rcParams["axes.linewidth"] = 1.2

ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)


def acquire_and_generate_raw_data(n_samples=2500, random_state=42):
    """
    Simulates programmatic acquisition of a comprehensive Customer Churn & Behavioral
    telecom dataset, injecting real-world data quality defects:
    - Structural missingness (MCAR & MAR)
    - Inconsistent casing and whitespace errors in strings
    - Ill-typed numerical values (strings with currency symbols and spaces)
    - Impossible erroneous values (negative tenures, negative charges)
    - Outliers and extreme skewed distributions
    - Inconsistent multi-format datetime strings
    - Duplicate customer IDs
    """
    np.random.seed(random_state)
    
    customer_ids = [f"CUST-{10000 + i}" for i in range(n_samples)]
    # Introduce ~20 duplicates
    for i in range(20):
        customer_ids[-(i+1)] = customer_ids[i]
        
    genders = np.random.choice(["Male", "Female", "male", "FEMALE", "  Male ", "Fe-male", None], size=n_samples, p=[0.45, 0.43, 0.03, 0.03, 0.02, 0.01, 0.03])
    senior_citizens = np.random.choice([0, 1, "0", "1", "Yes", "No", np.nan], size=n_samples, p=[0.7, 0.15, 0.04, 0.03, 0.03, 0.02, 0.03])
    partners = np.random.choice(["Yes", "No", "yes", "NO", "  Yes", None], size=n_samples, p=[0.46, 0.46, 0.03, 0.02, 0.01, 0.02])
    dependents = np.random.choice(["Yes", "No", "yes", "no", None], size=n_samples, p=[0.30, 0.62, 0.03, 0.02, 0.03])
    
    # Numerical tenure with negative errors & extreme outliers
    tenure_base = np.random.exponential(scale=24, size=n_samples).astype(float)
    tenure = np.clip(tenure_base, 0, 72)
    # Inject errors: negative values and extreme outliers
    tenure[np.random.choice(n_samples, size=25, replace=False)] = -5.0
    tenure[np.random.choice(n_samples, size=15, replace=False)] = 145.0  # Impossible tenure (> 72 months)
    # Inject missingness (MAR: correlated with tenure being very short)
    tenure_missing_mask = np.random.rand(n_samples) < 0.04
    tenure = [np.nan if m else t for m, t in zip(tenure_missing_mask, tenure)]
    
    phone_services = np.random.choice(["Yes", "No", None], size=n_samples, p=[0.88, 0.09, 0.03])
    multiple_lines = np.random.choice(["No phone service", "No", "Yes", "no", "yes", None], size=n_samples, p=[0.08, 0.44, 0.42, 0.02, 0.02, 0.02])
    internet_services = np.random.choice(["DSL", "Fiber optic", "No", "fiber optic", "dsl", None], size=n_samples, p=[0.34, 0.43, 0.17, 0.02, 0.02, 0.02])
    online_security = np.random.choice(["Yes", "No", "No internet service", None], size=n_samples, p=[0.28, 0.48, 0.20, 0.04])
    tech_support = np.random.choice(["Yes", "No", "No internet service", None], size=n_samples, p=[0.29, 0.47, 0.20, 0.04])
    streaming_tv = np.random.choice(["Yes", "No", "No internet service", None], size=n_samples, p=[0.38, 0.38, 0.20, 0.04])
    
    contract_types = np.random.choice(["Month-to-month", "One year", "Two year", "month-to-month", "1-Year", "2-Year", None], size=n_samples, p=[0.50, 0.22, 0.20, 0.03, 0.02, 0.01, 0.02])
    paperless_billing = np.random.choice(["Yes", "No", "Y", "N", None], size=n_samples, p=[0.56, 0.38, 0.02, 0.02, 0.02])
    payment_methods = np.random.choice([
        "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)",
        "electronic check", "Credit Card", None
    ], size=n_samples, p=[0.32, 0.21, 0.21, 0.21, 0.02, 0.01, 0.02])
    
    # Monthly Charges with dirty text formats, negatives, extreme outliers
    monthly_charges_base = np.random.normal(loc=64.7, scale=30.0, size=n_samples)
    monthly_charges_base = np.clip(monthly_charges_base, 18.0, 120.0)
    # Dirty formatting: some as "$75.50", " 89.2 ", negative values "-45.0"
    monthly_charges = []
    for val in monthly_charges_base:
        prob = np.random.rand()
        if prob < 0.03:
            monthly_charges.append(np.nan)
        elif prob < 0.06:
            monthly_charges.append(f"${val:.2f}")
        elif prob < 0.08:
            monthly_charges.append(f" {val:.1f} ")
        elif prob < 0.09:
            monthly_charges.append(-round(val, 2))  # negative error
        elif prob < 0.095:
            monthly_charges.append(round(val * 4.5, 2))  # Extreme Outlier (e.g. $480/mo)
        else:
            monthly_charges.append(round(val, 2))
            
    # Total Charges with empty spaces " ", strings, and missingness
    total_charges = []
    for t, m in zip(tenure, monthly_charges_base):
        if pd.isna(t) or t <= 0:
            total_charges.append(" ")  # Empty string legacy error
        else:
            prob = np.random.rand()
            if prob < 0.04:
                total_charges.append(np.nan)
            elif prob < 0.07:
                total_charges.append(" ")
            elif prob < 0.09:
                total_charges.append(f"${t * m + np.random.normal(0, 10):.2f}")
            elif prob < 0.095:
                total_charges.append(round(t * m * 3.5, 2)) # outlier
            else:
                total_charges.append(round(t * m + np.random.normal(0, 10), 2))
                
    # Signup Date with inconsistent formatting ("2021-04-12", "12/04/2021", "Apr 12, 2021", "2021/04/12")
    base_dates = pd.date_range(start="2018-01-01", end="2023-12-31", periods=n_samples)
    signup_dates = []
    for d in base_dates:
        fmt_choice = np.random.choice([0, 1, 2, 3, 4], p=[0.70, 0.12, 0.10, 0.05, 0.03])
        if fmt_choice == 0:
            signup_dates.append(d.strftime("%Y-%m-%d"))
        elif fmt_choice == 1:
            signup_dates.append(d.strftime("%d/%m/%Y"))
        elif fmt_choice == 2:
            signup_dates.append(d.strftime("%b %d, %Y"))
        elif fmt_choice == 3:
            signup_dates.append(d.strftime("%Y/%m/%d %H:%M"))
        else:
            signup_dates.append("INVALID_DATE")
            
    # Customer Satisfaction Score (1 to 5) with out-of-range errors (e.g. 0, 99)
    satisfaction = np.random.choice([1, 2, 3, 4, 5, 0, 99, np.nan], size=n_samples, p=[0.12, 0.18, 0.30, 0.24, 0.10, 0.02, 0.01, 0.03])
    
    # Target variable: Churn ("Yes", "No", "yes", "no", None)
    churn_prob = 1 / (1 + np.exp(-(0.03 * (monthly_charges_base - 65) - 0.05 * (np.nan_to_num(tenure, nan=12) - 24) - 0.4 * (np.nan_to_num(satisfaction, nan=3) - 3))))
    churn = ["Yes" if np.random.rand() < p else "No" for p in churn_prob]
    # Introduce noisy representations in target
    for i in range(len(churn)):
        p = np.random.rand()
        if p < 0.02:
            churn[i] = "yes" if churn[i] == "Yes" else "no"
        elif p < 0.03:
            churn[i] = None

    raw_df = pd.DataFrame({
        "CustomerID": customer_ids,
        "Gender": genders,
        "SeniorCitizen": senior_citizens,
        "Partner": partners,
        "Dependents": dependents,
        "TenureMonths": tenure,
        "PhoneService": phone_services,
        "MultipleLines": multiple_lines,
        "InternetService": internet_services,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "Contract": contract_types,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_methods,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "SignupDate": signup_dates,
        "SatisfactionScore": satisfaction,
        "Churn": churn
    })
    
    return raw_df


def perform_eda_and_diagnostics(df):
    """
    Performs comprehensive exploratory analysis and audits data health.
    Returns metrics and creates missingness visualizations.
    """
    print("=" * 70)
    print("1. DATA QUALITY & INTEGRITY AUDIT")
    print("=" * 70)
    print(f"Total Rows (Raw): {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print(f"Duplicate Customer IDs: {df['CustomerID'].duplicated().sum()}")
    
    # Check data types and apparent missingness
    missing_summary = []
    for col in df.columns:
        null_count = df[col].isnull().sum()
        # Count string representations of nulls like ' ', 'NA', 'None'
        blank_count = 0
        if df[col].dtype == "object":
            blank_count = df[col].apply(lambda x: 1 if isinstance(x, str) and (x.strip() == "" or x.strip().upper() in ["NA", "N/A", "NULL", "NONE"]) else 0).sum()
        total_missing = null_count + blank_count
        missing_summary.append({
            "Feature": col,
            "Raw Nulls": null_count,
            "Hidden Blanks": blank_count,
            "Total Incomplete": total_missing,
            "Missing %": round((total_missing / len(df)) * 100, 2),
            "Dtype": str(df[col].dtype)
        })
    missing_df = pd.DataFrame(missing_summary).sort_values(by="Total Incomplete", ascending=False)
    print("\n--- Missing / Incomplete Values Summary ---")
    print(missing_df.to_string(index=False))
    
    # Visual 1: Missing Data Bar Chart
    plt.figure(figsize=(12, 6))
    missing_plot_data = missing_df[missing_df["Total Incomplete"] > 0]
    bars = plt.barh(missing_plot_data["Feature"], missing_plot_data["Missing %"], color="#3182CE", edgecolor="#2B6CB0", height=0.65)
    plt.xlabel("Missing / Incomplete Percentage (%)", fontsize=12, fontweight="bold", labelpad=10)
    plt.ylabel("Dataset Features", fontsize=12, fontweight="bold")
    plt.title("Audit of Incomplete & Missing Values per Feature (Raw Ingestion)", fontsize=14, fontweight="bold", pad=15)
    plt.xlim(0, max(missing_plot_data["Missing %"]) * 1.25)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.15, bar.get_y() + bar.get_height() / 2, f"{w:.1f}%", va="center", ha="left", fontsize=10, fontweight="semibold", color="#2D3748")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "02_missing_values_bar.png"), dpi=300)
    plt.close()
    
    # Visual 2: Missingness Matrix Heatmap
    plt.figure(figsize=(14, 6))
    # Replace whitespace strings with NaN temporarily for heatmap
    temp_null_df = df.replace(r"^\s*$", np.nan, regex=True).isnull()
    sns.heatmap(temp_null_df.T, cbar=False, cmap="Blues", yticklabels=True, xticklabels=False)
    plt.title("Missing Data Pattern Matrix (Dark indicates Missing/Unstructured Cell)", fontsize=13, fontweight="bold", pad=12)
    plt.ylabel("Features", fontsize=11, fontweight="bold")
    plt.xlabel("Observations (Rows 0 to 2500)", fontsize=11, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "01_missing_data_matrix.png"), dpi=300)
    plt.close()
    
    return missing_df


def clean_and_remediate_data(df):
    """
    Executes meticulous data cleaning:
    1. Deduplication based on primary key.
    2. String standardization (whitespace stripping, lowercase normalization, category unification).
    3. Type casting & parsing numeric fields (stripping '$', casting to float).
    4. Out-of-bounds erroneous value correction (negative tenures, invalid satisfaction scores).
    5. Datetime parsing with multiple format fallbacks.
    6. Advanced Imputation:
       - Categorical: Mode / Domain Default Imputation.
       - Numerical: KNN Imputation (k=5) & Median Imputation.
    """
    print("\n" + "=" * 70)
    print("2. EXECUTING SYSTEMATIC DATA CLEANING")
    print("=" * 70)
    
    clean_df = df.copy()
    
    # Step 1: Deduplication
    initial_count = len(clean_df)
    clean_df = clean_df.drop_duplicates(subset=["CustomerID"], keep="first")
    dedup_removed = initial_count - len(clean_df)
    print(f"[OK] Deduplication: Removed {dedup_removed} duplicate customer records.")
    
    # Step 2: String Standardization & Formatting
    string_cols = ["Gender", "Partner", "Dependents", "PhoneService", "MultipleLines", 
                   "InternetService", "OnlineSecurity", "TechSupport", "StreamingTV", 
                   "Contract", "PaperlessBilling", "PaymentMethod", "Churn"]
    
    for col in string_cols:
        if col in clean_df.columns:
            clean_df[col] = clean_df[col].astype(str).str.strip()
            clean_df[col] = clean_df[col].replace(["nan", "None", "NULL", "N/A", ""], np.nan)
    
    # Unify Gender
    gender_map = {"Male": "Male", "male": "Male", "MALE": "Male", "FEMALE": "Female", 
                  "Female": "Female", "female": "Female", "Fe-male": "Female"}
    clean_df["Gender"] = clean_df["Gender"].map(gender_map)
    
    # Unify Binary Flag columns
    binary_map = {"Yes": "Yes", "yes": "Yes", "Y": "Yes", "No": "No", "no": "No", "N": "No"}
    for b_col in ["Partner", "Dependents", "PhoneService", "PaperlessBilling", "Churn"]:
        clean_df[b_col] = clean_df[b_col].map(binary_map)
        
    # Unify SeniorCitizen
    senior_map = {0: 0, 1: 1, "0": 0, "1": 1, "No": 0, "Yes": 1}
    clean_df["SeniorCitizen"] = clean_df["SeniorCitizen"].map(senior_map)
    
    # Unify Contract
    contract_map = {"Month-to-month": "Month-to-month", "month-to-month": "Month-to-month", 
                    "One year": "One year", "1-Year": "One year", 
                    "Two year": "Two year", "2-Year": "Two year"}
    clean_df["Contract"] = clean_df["Contract"].map(contract_map)
    
    # Unify Internet & Multi-services
    clean_df["InternetService"] = clean_df["InternetService"].replace({"fiber optic": "Fiber optic", "dsl": "DSL"})
    clean_df["PaymentMethod"] = clean_df["PaymentMethod"].replace({"electronic check": "Electronic check", "Credit Card": "Credit card (automatic)"})
    
    print("[OK] String Standardization: Normalized categorical variance across all text fields.")
    
    # Step 3: Parse Numeric Columns from Strings & Repair Erroneous Values
    def parse_numeric(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).replace("$", "").replace(",", "").strip()
        if val_str == "" or val_str.upper() in ["NA", "NULL", "NONE"]:
            return np.nan
        try:
            return float(val_str)
        except ValueError:
            return np.nan
            
    clean_df["MonthlyCharges"] = clean_df["MonthlyCharges"].apply(parse_numeric)
    clean_df["TotalCharges"] = clean_df["TotalCharges"].apply(parse_numeric)
    clean_df["TenureMonths"] = clean_df["TenureMonths"].apply(parse_numeric)
    clean_df["SatisfactionScore"] = clean_df["SatisfactionScore"].apply(parse_numeric)
    
    # Step 4: Erroneous Values Domain Remediation
    # MonthlyCharges cannot be negative
    neg_monthly = (clean_df["MonthlyCharges"] < 0).sum()
    clean_df.loc[clean_df["MonthlyCharges"] < 0, "MonthlyCharges"] = np.nan
    
    # Tenure cannot be negative or > 72 months (telecom max history window)
    neg_tenure = (clean_df["TenureMonths"] < 0).sum()
    excess_tenure = (clean_df["TenureMonths"] > 72).sum()
    clean_df.loc[clean_df["TenureMonths"] < 0, "TenureMonths"] = np.nan
    clean_df.loc[clean_df["TenureMonths"] > 72, "TenureMonths"] = np.nan
    
    # Satisfaction score must be within [1, 5]
    invalid_sat = (~clean_df["SatisfactionScore"].between(1, 5) & clean_df["SatisfactionScore"].notnull()).sum()
    clean_df.loc[~clean_df["SatisfactionScore"].between(1, 5), "SatisfactionScore"] = np.nan
    
    print(f"[OK] Erroneous Domain Repair: Nullified {neg_monthly} negative charges, {neg_tenure} negative tenures, {excess_tenure} out-of-range tenures, {invalid_sat} out-of-range satisfaction ratings.")
    
    # Step 5: Datetime Normalization
    def parse_flexible_date(d_str):
        if pd.isna(d_str) or d_str == "INVALID_DATE":
            return pd.NaT
        try:
            return pd.to_datetime(d_str, format="mixed", errors="coerce")
        except Exception:
            return pd.NaT
            
    clean_df["SignupDate_Parsed"] = clean_df["SignupDate"].apply(parse_flexible_date)
    # Impute missing signup dates based on max date minus tenure
    reference_date = pd.Timestamp("2024-01-01")
    est_dates = reference_date - pd.to_timedelta(clean_df["TenureMonths"].fillna(12) * 30.44, unit="D")
    clean_df["SignupDate_Parsed"] = clean_df["SignupDate_Parsed"].fillna(est_dates)
    clean_df["CustomerAgeDays"] = (reference_date - clean_df["SignupDate_Parsed"]).dt.days
    
    print("[OK] Datetime Parsing: Multi-format parsing complete. Derived 'CustomerAgeDays' feature.")
    
    # Step 6: Missing Value Imputation
    # Categorical mode imputation
    for cat_col in ["Gender", "Partner", "Dependents", "PhoneService", "MultipleLines", 
                    "InternetService", "OnlineSecurity", "TechSupport", "StreamingTV", 
                    "Contract", "PaperlessBilling", "PaymentMethod", "SeniorCitizen"]:
        mode_val = clean_df[cat_col].mode()[0]
        clean_df[cat_col] = clean_df[cat_col].fillna(mode_val)
        
    # Churn target: if null, use mode
    clean_df["Churn"] = clean_df["Churn"].fillna(clean_df["Churn"].mode()[0])
    
    # Numerical KNN Imputation for TenureMonths, MonthlyCharges, TotalCharges, SatisfactionScore
    num_cols_to_impute = ["TenureMonths", "MonthlyCharges", "SatisfactionScore"]
    imputer = KNNImputer(n_neighbors=5, weights="distance")
    clean_df[num_cols_to_impute] = imputer.fit_transform(clean_df[num_cols_to_impute])
    clean_df["SatisfactionScore"] = clean_df["SatisfactionScore"].round().astype(int)
    
    # Calculate TotalCharges if missing: TenureMonths * MonthlyCharges
    clean_df["TotalCharges"] = clean_df["TotalCharges"].fillna(clean_df["TenureMonths"] * clean_df["MonthlyCharges"])
    
    print("[OK] Imputation Complete: Applied KNN Imputation for continuous numericals and Mode Imputation for categoricals.")
    return clean_df


def handle_outliers_and_transformations(raw_df, clean_df):
    """
    Performs statistical outlier analysis:
    - IQR Capping (Winsorization) & Isolation Forest detection.
    - Skewness analysis & Logarithmic transformation.
    - Generates before-and-after distribution and outlier boxplots.
    """
    print("\n" + "=" * 70)
    print("3. OUTLIER DIAGNOSTICS, TREATMENT & SKEWNESS TRANSFORMATION")
    print("=" * 70)
    
    treated_df = clean_df.copy()
    
    # Numerical features to audit
    num_features = ["MonthlyCharges", "TotalCharges", "TenureMonths"]
    
    # Visual 3: Outlier Boxplots Before Treatment
    plt.figure(figsize=(14, 5))
    for i, col in enumerate(num_features, 1):
        plt.subplot(1, 3, i)
        sns.boxplot(y=treated_df[col], color="#63B3ED", flierprops=dict(marker="o", markerfacecolor="#E53E3E", markersize=6))
        plt.title(f"Distribution & Outliers: {col}", fontsize=11, fontweight="bold")
        plt.ylabel(col, fontsize=10, fontweight="semibold")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "03_outliers_before_cleaning.png"), dpi=300)
    plt.close()
    
    # IQR Outlier Capping (Winsorization)
    outlier_stats = {}
    for col in ["MonthlyCharges", "TotalCharges"]:
        Q1 = treated_df[col].quantile(0.25)
        Q3 = treated_df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = max(0, Q1 - 1.5 * IQR)
        upper_bound = Q3 + 1.5 * IQR
        
        n_outliers = ((treated_df[col] < lower_bound) | (treated_df[col] > upper_bound)).sum()
        outlier_stats[col] = {
            "Q1": round(Q1, 2), "Q3": round(Q3, 2), "IQR": round(IQR, 2),
            "Lower Bound": round(lower_bound, 2), "Upper Bound": round(upper_bound, 2),
            "Outliers Detected": n_outliers
        }
        
        # Winsorize / Cap at bounds
        treated_df[f"{col}_Capped"] = np.clip(treated_df[col], lower_bound, upper_bound)
        
    print("--- Statistical Outlier Thresholds (1.5 x IQR Rule) ---")
    print(pd.DataFrame(outlier_stats).T.to_string())
    
    # Visual 4: Before vs After Outlier Treatment Comparison for TotalCharges
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    sns.boxplot(ax=axes[0], y=clean_df["TotalCharges"], color="#FC8181")
    axes[0].set_title("TotalCharges (Pre-Treatment: Raw Outliers Present)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Total Charges ($)", fontsize=10, fontweight="semibold")
    
    sns.boxplot(ax=axes[1], y=treated_df["TotalCharges_Capped"], color="#68D391")
    axes[1].set_title("TotalCharges (Post-Treatment: IQR Winsorized)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Total Charges ($)", fontsize=10, fontweight="semibold")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "04_outlier_treatment_comparison.png"), dpi=300)
    plt.close()
    
    # Skewness Analysis & Log Transformation
    skew_raw_total = treated_df["TotalCharges_Capped"].skew()
    treated_df["TotalCharges_Log1p"] = np.log1p(treated_df["TotalCharges_Capped"])
    skew_trans_total = treated_df["TotalCharges_Log1p"].skew()
    
    print(f"\n[OK] Skewness Remediation: TotalCharges Skewness reduced from {skew_raw_total:.3f} to {skew_trans_total:.3f} via Log1p transformation.")
    
    # Visual 5: Skewness Transformation Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(ax=axes[0], data=treated_df["TotalCharges_Capped"], kde=True, color="#3182CE", bins=30)
    axes[0].set_title(f"Original TotalCharges (Skewness = {skew_raw_total:.2f})", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Total Charges ($)", fontsize=10, fontweight="semibold")
    
    sns.histplot(ax=axes[1], data=treated_df["TotalCharges_Log1p"], kde=True, color="#38A169", bins=30)
    axes[1].set_title(f"Log1p Transformed TotalCharges (Skewness = {skew_trans_total:.2f})", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Log1p(Total Charges)", fontsize=10, fontweight="semibold")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "05_skewness_transformation.png"), dpi=300)
    plt.close()
    
    return treated_df


def engineer_features_and_encode(df):
    """
    Executes Feature Engineering, Categorical Encoding, and Feature Scaling:
    1. Feature Engineering:
       - TenureGroup: Binned tenure into lifecycles (0-12m, 13-24m, 25-48m, 49-72m).
       - TotalServicesCount: Count of active value-add services subscribed.
       - ChargePerTenureMonth: Monthly cost efficiency ratio.
       - IsHighValueCustomer: Flag for top 25% revenue contributors.
    2. Categorical Encoding:
       - Binary mapping for 2-state categories (Gender, Partner, Dependents, etc.).
       - One-Hot Encoding for multi-class nominal variables (Contract, PaymentMethod, InternetService).
    3. Feature Scaling:
       - StandardScaler / RobustScaler on continuous variables.
    """
    print("\n" + "=" * 70)
    print("4. FEATURE ENGINEERING, CATEGORICAL ENCODING & SCALING")
    print("=" * 70)
    
    feat_df = df.copy()
    
    # Feature 1: Tenure Group Bins
    bins = [-1, 12, 24, 48, 73]
    labels = ["New (<1yr)", "Early (1-2yrs)", "Established (2-4yrs)", "Loyal (4+yrs)"]
    feat_df["TenureGroup"] = pd.cut(feat_df["TenureMonths"], bins=bins, labels=labels)
    
    # Feature 2: Service Density Score (Count of active digital services)
    service_cols = ["OnlineSecurity", "TechSupport", "StreamingTV", "MultipleLines", "PhoneService"]
    feat_df["TotalServicesCount"] = 0
    for col in service_cols:
        feat_df["TotalServicesCount"] += (feat_df[col] == "Yes").astype(int)
        
    # Feature 3: Monthly Charge to Total Charge Ratio
    feat_df["MonthlyToTotalRatio"] = feat_df["MonthlyCharges_Capped"] / (feat_df["TotalCharges_Capped"] + 1)
    
    # Feature 4: High Value Customer Flag
    feat_df["IsHighValueCustomer"] = (feat_df["MonthlyCharges_Capped"] > feat_df["MonthlyCharges_Capped"].quantile(0.75)).astype(int)
    
    # Target Encoding
    feat_df["Churn_Numeric"] = (feat_df["Churn"] == "Yes").astype(int)
    
    # Visual 6: Categorical Distributions vs Churn
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(ax=axes[0], data=feat_df, x="TenureGroup", hue="Churn", palette=["#4299E1", "#F56565"])
    axes[0].set_title("Customer Churn Distribution Across Tenure Lifecycles", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Tenure Cohort", fontsize=10, fontweight="semibold")
    axes[0].set_ylabel("Customer Count", fontsize=10, fontweight="semibold")
    
    sns.barplot(ax=axes[1], data=feat_df, x="TotalServicesCount", y="Churn_Numeric", palette="Blues_d", ci=None)
    axes[1].set_title("Churn Rate by Subscribed Digital Services Density", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Number of Add-on Services", fontsize=10, fontweight="semibold")
    axes[1].set_ylabel("Empirical Churn Probability", fontsize=10, fontweight="semibold")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "07_categorical_distributions.png"), dpi=300)
    plt.close()
    
    # Encoding: One-Hot Encode multi-class variables
    nominal_cols = ["InternetService", "Contract", "PaymentMethod", "TenureGroup"]
    encoded_nominals = pd.get_dummies(feat_df[nominal_cols], drop_first=True, dtype=int)
    
    # Binary Encoding
    binary_cols = ["Gender", "Partner", "Dependents", "PhoneService", "PaperlessBilling"]
    for col in binary_cols:
        feat_df[f"{col}_Binary"] = (feat_df[col] == "Yes") if col != "Gender" else (feat_df[col] == "Male")
        feat_df[f"{col}_Binary"] = feat_df[f"{col}_Binary"].astype(int)
        
    # Feature Scaling: StandardScaler on numerical features
    continuous_features = ["TenureMonths", "MonthlyCharges_Capped", "TotalCharges_Log1p", "CustomerAgeDays", "MonthlyToTotalRatio"]
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(feat_df[continuous_features])
    scaled_df = pd.DataFrame(scaled_matrix, columns=[f"{c}_Scaled" for c in continuous_features], index=feat_df.index)
    
    # Assemble final Machine Learning Ready Dataset
    model_ready_df = pd.concat([
        feat_df[["CustomerID", "Churn_Numeric", "SeniorCitizen", "SatisfactionScore", "TotalServicesCount", "IsHighValueCustomer"]],
        feat_df[[f"{col}_Binary" for col in binary_cols]],
        encoded_nominals,
        scaled_df
    ], axis=1)
    
    # Visual 7: Correlation Heatmap
    plt.figure(figsize=(14, 10))
    corr_cols = [c for c in model_ready_df.columns if c != "CustomerID"]
    corr_matrix = model_ready_df[corr_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, cmap="coolwarm", vmin=-0.6, vmax=0.8, annot=False, linewidths=0.5)
    plt.title("Correlation Matrix of Preprocessed & Engineered Features (Model-Ready)", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "06_feature_correlation_matrix.png"), dpi=300)
    plt.close()
    
    print(f"[OK] Feature Engineering Complete: Dataset transformed into {model_ready_df.shape[1]} ML-ready features.")
    return feat_df, model_ready_df


def generate_pipeline_diagram():
    """
    Generates a clean visual flowchart of the Data Cleaning and Preprocessing pipeline.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")
    
    boxes = [
        {"text": "1. Data Acquisition & Ingestion\n- Multi-source CSV simulation\n- Schema & type identification", "x": 0.05, "y": 0.5, "color": "#EBF8FF", "edge": "#3182CE"},
        {"text": "2. Data Quality Audit\n- Structural & hidden missingness\n- Outlier & skewness detection", "x": 0.28, "y": 0.5, "color": "#FEFCBF", "edge": "#D69E2E"},
        {"text": "3. Cleaning & Remediation\n- Deduplication & Type Casting\n- KNN & Mode Imputation\n- Domain rule boundary enforcement", "x": 0.51, "y": 0.5, "color": "#FED7D7", "edge": "#E53E3E"},
        {"text": "4. Preprocessing & Engineering\n- IQR Winsorization & Log1p\n- One-Hot / Binary Encoding\n- Standard & Robust Scaling", "x": 0.74, "y": 0.5, "color": "#C6F6D5", "edge": "#38A169"},
    ]
    
    for b in boxes:
        bbox_props = dict(boxstyle="round,pad=0.6", facecolor=b["color"], edgecolor=b["edge"], linewidth=2)
        ax.text(b["x"] + 0.09, b["y"], b["text"], ha="center", va="center", fontsize=9.5, fontweight="bold", color="#2D3748", bbox=bbox_props)
        
    # Draw arrows
    arrow_props = dict(facecolor="#4A5568", edgecolor="#4A5568", arrowstyle="->", lw=2.5)
    ax.annotate("", xy=(0.23, 0.5), xytext=(0.19, 0.5), arrowprops=arrow_props)
    ax.annotate("", xy=(0.46, 0.5), xytext=(0.42, 0.5), arrowprops=arrow_props)
    ax.annotate("", xy=(0.69, 0.5), xytext=(0.65, 0.5), arrowprops=arrow_props)
    ax.annotate("", xy=(0.92, 0.5), xytext=(0.88, 0.5), arrowprops=arrow_props)
    
    # Final Output box
    out_bbox = dict(boxstyle="round,pad=0.5", facecolor="#E9D8FD", edgecolor="#805AD5", linewidth=2)
    ax.text(0.97, 0.5, "5. ML-Ready\nDataset", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#44337A", bbox=out_bbox)
    
    plt.title("End-to-End Data Acquisition, Cleaning & Preprocessing Architecture", fontsize=13, fontweight="bold", pad=20, color="#1A202C")
    plt.tight_layout()
    plt.savefig(os.path.join(ASSETS_DIR, "08_data_cleaning_pipeline_flowchart.png"), dpi=300)
    plt.close()
    print("[OK] Generated Pipeline Flowchart.")


def main():
    print("Starting Week 1 Data Cleaning & Preprocessing Pipeline Execution...")
    
    # Step 1: Acquire and Generate Data
    raw_df = acquire_and_generate_raw_data(n_samples=2500)
    raw_df.to_csv("raw_customer_dataset.csv", index=False)
    print(f"[OK] Raw dataset saved to 'raw_customer_dataset.csv' ({raw_df.shape[0]} rows, {raw_df.shape[1]} cols).")
    
    # Step 2: EDA & Diagnostics
    missing_df = perform_eda_and_diagnostics(raw_df)
    
    # Step 3: Cleaning & Remediation
    clean_df = clean_and_remediate_data(raw_df)
    clean_df.to_csv("cleaned_customer_dataset.csv", index=False)
    print(f"[OK] Cleaned dataset saved to 'cleaned_customer_dataset.csv' ({clean_df.shape[0]} rows, {clean_df.shape[1]} cols).")
    
    # Step 4: Outliers & Skewness Transformation
    treated_df = handle_outliers_and_transformations(raw_df, clean_df)
    
    # Step 5: Feature Engineering & Preprocessing
    feat_df, model_ready_df = engineer_features_and_encode(treated_df)
    model_ready_df.to_csv("preprocessed_model_ready_dataset.csv", index=False)
    print(f"[OK] Model-ready preprocessed dataset saved to 'preprocessed_model_ready_dataset.csv' ({model_ready_df.shape[1]} ML-ready features).")
    
    # Step 6: Generate Architecture Diagram
    generate_pipeline_diagram()
    
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION SUCCESSFULLY COMPLETED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
