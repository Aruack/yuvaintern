# Week 1 Task: Data Acquisition, Cleaning, and Preprocessing

**Program**: Virtual Data Science with Python Trainee | YuvaInternship  
**Author**: Aryan Kumar  
**Domain**: Customer Intelligence & Churn Analytics  
**Core Technologies**: Python 3.13, Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, python-docx  

---

## 📋 Executive Overview
This repository contains the complete deliverables for the **Week 1 Task: Data Acquisition, Cleaning, and Preprocessing**. The objective of this project is to demonstrate end-to-end data science capabilities: acquiring a publicly available benchmark dataset, diagnosing complex data quality issues (hidden missingness, impossible values, heterogeneous formatting, outliers, and skewness), executing systematic multi-stage data cleaning and remediation, performing feature engineering, and producing a publication-grade formal technical report.

---

## 🗂️ Deliverables & Directory Structure

```
├── Week_1_Data_Acquisition_Cleaning_Report.docx  # Primary Deliverable: Formal Technical Report
├── Week_1_Data_Cleaning_and_Preprocessing.ipynb # Interactive Jupyter Notebook
├── data_preprocessing_pipeline.py               # Complete End-to-End Python Pipeline Script
├── generate_report.py                           # Automated DOCX Report Generator Script
├── create_notebook.py                           # Jupyter Notebook Builder Script
├── raw_customer_dataset.csv                     # Ingested Raw Dataset with Real-World Noise
├── cleaned_customer_dataset.csv                 # Cleaned, Remediated & Imputed Dataset
├── preprocessed_model_ready_dataset.csv         # 26 ML-Ready Features (Scaled & Encoded)
├── README.md                                    # Project Documentation
└── assets/                                      # Diagnostic Visualizations (High-Res 300 DPI)
    ├── 01_missing_data_matrix.png
    ├── 02_missing_values_bar.png
    ├── 03_outliers_before_cleaning.png
    ├── 04_outlier_treatment_comparison.png
    ├── 05_skewness_transformation.png
    ├── 06_feature_correlation_matrix.png
    ├── 07_categorical_distributions.png
    └── 08_data_cleaning_pipeline_flowchart.png
```

---

## 🚀 Key Preprocessing Highlights

1. **Hidden Missingness Detection**: Audited both explicit `NaN` values and concealed blank strings (`" "`, `"N/A"`, `"NULL"`), uncovering that `TotalCharges` had 11.44% true incomplete records.
2. **Deterministic & KNN Imputation**:
   - Categorical attributes: Mode imputation.
   - Continuous numerical attributes (`TenureMonths`, `MonthlyCharges`, `SatisfactionScore`): 5-Nearest Neighbors (`KNNImputer`) with distance weighting.
   - Relational features: Reconstructed missing `TotalCharges` via `TenureMonths * MonthlyCharges`.
3. **Domain Constraint Enforcement**:
   - Eradicated negative monthly charges and negative tenures.
   - Constrained tenure to maximum operational historical threshold (72 months).
   - Clipped out-of-range satisfaction ratings (e.g. 0, 99) to the standard [1, 5] Likert scale.
4. **Outlier Remediation**:
   - Tukey 1.5× IQR detection with **Winsorization (Robust Boundary Capping)** to prevent sample loss.
5. **Distributional Transformation**:
   - Stabilized right-skewed `TotalCharges` (+1.063 skewness) via `Log1p` transformation.
6. **Feature Engineering & ML Readiness**:
   - Engineered `TenureGroup` (lifecycle cohorts), `TotalServicesCount` (ecosystem stickiness), `MonthlyToTotalRatio` (billing shock indicator), and `IsHighValueCustomer`.
   - Applied One-Hot Encoding (`drop_first=True`) and `StandardScaler` to produce 26 model-ready features.

---

## 🛠️ Execution Instructions

To execute the data cleaning pipeline and generate all assets and datasets:
```bash
python data_preprocessing_pipeline.py
```

To compile the Microsoft Word technical report (`.docx`):
```bash
python generate_report.py
```

To rebuild the Jupyter Notebook:
```bash
python create_notebook.py
```
