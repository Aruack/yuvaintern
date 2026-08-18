"""
generate_diagrams.py
Generates 4 publication-quality architectural and workflow diagrams for the 
Machine Learning Model Development and Evaluation Plan.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

# Configure aesthetic parameters
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

output_dir = os.path.dirname(os.path.abspath(__file__))

def create_box(ax, x, y, width, height, title, subtitle="", color="#1B365D", text_color="white", sub_color="#D1E8E2", box_style="round,pad=0.3,rounding_size=0.15", linewidth=1.5, edgecolor=None):
    if edgecolor is None:
        edgecolor = color
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle=box_style,
                         facecolor=color,
                         edgecolor=edgecolor,
                         linewidth=linewidth,
                         zorder=3)
    ax.add_patch(box)
    
    if subtitle:
        ax.text(x + width/2, y + height*0.62, title,
                ha='center', va='center', color=text_color,
                fontsize=9.5, fontweight='bold', zorder=4)
        ax.text(x + width/2, y + height*0.30, subtitle,
                ha='center', va='center', color=sub_color,
                fontsize=7.5, zorder=4, style='italic')
    else:
        ax.text(x + width/2, y + height/2, title,
                ha='center', va='center', color=text_color,
                fontsize=9, fontweight='bold', zorder=4)
    return box

def draw_arrow(ax, start, end, label="", color="#4B6B94", width=1.5, style="->", connectionstyle="arc3,rad=0.0", label_offset=(0, 0)):
    arrow = patches.FancyArrowPatch(start, end,
                                    arrowstyle=f"-|>,head_length=5,head_width=3",
                                    color=color,
                                    linewidth=width,
                                    connectionstyle=connectionstyle,
                                    zorder=2)
    ax.add_patch(arrow)
    if label:
        mid_x = (start[0] + end[0]) / 2 + label_offset[0]
        mid_y = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mid_x, mid_y, label, ha='center', va='center',
                fontsize=7.5, color="#1B365D", fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85),
                zorder=5)

# ==============================================================================
# Diagram 1: End-to-End ML System Lifecycle Architecture
# ==============================================================================
def generate_lifecycle_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Title
    ax.text(6, 6.6, "End-to-End Enterprise Machine Learning System Lifecycle",
            ha='center', va='center', fontsize=14, fontweight='bold', color="#0D233A")
    ax.text(6, 6.25, "Systematic Phase-Wise Blueprint from Problem Formulation to Continuous Feedback Loop",
            ha='center', va='center', fontsize=9, color="#555555", style='italic')
    
    # Phase 1: Problem Definition & Data Sourcing
    create_box(ax, 0.5, 4.4, 2.3, 1.3, "1. Ingestion & Inception", "• Problem Definition & KPIs\n• Multi-source ETL\n• Schema & Quality Check", color="#1B365D")
    
    # Phase 2: Exploratory Data Analysis & Preprocessing
    create_box(ax, 3.4, 4.4, 2.3, 1.3, "2. Preprocessing & EDA", "• Imputation & Outliers\n• Feature Engineering\n• Class Imbalance (SMOTE)", color="#2E6B9E")
    
    # Phase 3: Model Exploration & Selection
    create_box(ax, 6.3, 4.4, 2.3, 1.3, "3. Model Development", "• Candidate Algorithm Benchmarking\n• LightGBM / XGBoost / CatBoost\n• Loss & Regularization Setup", color="#008080")
    
    # Phase 4: Validation & Hyperparameter Tuning
    create_box(ax, 9.2, 4.4, 2.3, 1.3, "4. Tuning & Validation", "• Stratified Nested K-Fold\n• Optuna Bayesian HPO\n• PR-AUC / Cost-Benefit Matrix", color="#D96B27")
    
    # Phase 5: Explainability & Governance
    create_box(ax, 9.2, 1.8, 2.3, 1.3, "5. Explainability & Audit", "• SHAP Global & Local Values\n• Fairness & Bias Auditing\n• Model Card & Artifact Storage", color="#8E44AD")
    
    # Phase 6: Packaging & Deployment
    create_box(ax, 6.3, 1.8, 2.3, 1.3, "6. Model Deployment", "• FastAPI REST Service\n• Docker Containerization\n• Batch & Real-time Endpoints", color="#27AE60")
    
    # Phase 7: MLOps Monitoring & Retraining
    create_box(ax, 3.4, 1.8, 2.3, 1.3, "7. MLOps Monitoring", "• Data & Concept Drift (PSI/KS)\n• Performance Degradation\n• Automated Trigger Pipeline", color="#C0392B")

    # Connectors
    draw_arrow(ax, (2.8, 5.05), (3.4, 5.05), "Clean Data")
    draw_arrow(ax, (5.7, 5.05), (6.3, 5.05), "Features")
    draw_arrow(ax, (8.6, 5.05), (9.2, 5.05), "Models")
    draw_arrow(ax, (10.35, 4.4), (10.35, 3.1), "Best Model")
    draw_arrow(ax, (9.2, 2.45), (8.6, 2.45), "Approved")
    draw_arrow(ax, (6.3, 2.45), (5.7, 2.45), "Inference")
    
    # Feedback loop arrow from 7 back to 1
    arrow_fb = patches.FancyArrowPatch((3.4, 2.45), (1.65, 4.4),
                                       arrowstyle="-|>,head_length=6,head_width=4",
                                       color="#C0392B", linewidth=1.8,
                                       connectionstyle="arc3,rad=-0.25", zorder=2, linestyle='--')
    ax.add_patch(arrow_fb)
    ax.text(1.7, 2.9, "Continuous Feedback &\nAutomated Retraining", ha='center', va='center',
            fontsize=7.5, color="#C0392B", fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FDEDEC', edgecolor='#C0392B', alpha=0.9))

    plt.tight_layout()
    path = os.path.join(output_dir, "workflow_architecture.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

# ==============================================================================
# Diagram 2: Data Preprocessing and Feature Pipeline
# ==============================================================================
def generate_preprocessing_diagram():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5.5, 5.6, "Data Preprocessing & Feature Engineering Architecture",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#0D233A")
    ax.text(5.5, 5.25, "Sequential Data Pipeline ensuring Zero Leakage and High Feature Signal",
            ha='center', va='center', fontsize=8.5, color="#555555", style='italic')
    
    # Raw Data
    create_box(ax, 0.4, 2.2, 1.8, 2.0, "Raw Data Lake", "• Demographics\n• Account Specs\n• Usage Telemetry\n• Payment Logs\n• Support Tickets", color="#34495E")
    
    # Cleaning & Imputation
    create_box(ax, 2.7, 3.4, 2.3, 1.3, "Cleaning & Quality", "• KNN/Iterative Imputation\n• Isolation Forest Outliers\n• Schema & Type Casting", color="#2980B9")
    
    # Numerical Pipeline
    create_box(ax, 5.5, 3.4, 2.4, 1.3, "Numerical Pipeline", "• Yeo-Johnson Power Xform\n• RobustScaler / Z-Score\n• Usage Trend Ratios\n• Interaction Term Gen", color="#16A085")
    
    # Categorical Pipeline
    create_box(ax, 5.5, 1.3, 2.4, 1.3, "Categorical Pipeline", "• Smoothed Target Encoding\n• One-Hot (Low Cardinality)\n• Ordinal Tenure Binning\n• Frequency Encoding", color="#8E44AD")

    # Feature Selection & Balancing
    create_box(ax, 8.4, 2.2, 2.2, 2.0, "Selection & Resampling", "• Mutual Info & RFECV\n• Collinearity (VIF < 5)\n• SMOTE-NC (Train Only)\n• Final Clean Feature Matrix", color="#D35400")

    # Arrows
    draw_arrow(ax, (2.2, 3.6), (2.7, 4.05))
    draw_arrow(ax, (2.2, 2.8), (5.5, 1.95), connectionstyle="arc3,rad=-0.1")
    draw_arrow(ax, (5.0, 4.05), (5.5, 4.05))
    draw_arrow(ax, (7.9, 4.05), (8.4, 3.6))
    draw_arrow(ax, (7.9, 1.95), (8.4, 2.8))
    
    # Zero Leakage boundary box
    leakage_box = patches.Rectangle((2.5, 0.8), 8.3, 4.2, fill=False, edgecolor='#E74C3C', linestyle='--', linewidth=1.5)
    ax.add_patch(leakage_box)
    ax.text(6.65, 0.95, "Strict Train-Test Isolation Boundary (Zero Data Leakage Pipeline)", ha='center', fontsize=8, fontweight='bold', color='#C0392B')

    plt.tight_layout()
    path = os.path.join(output_dir, "preprocessing_pipeline.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

# ==============================================================================
# Diagram 3: Validation, Tuning & Model Evaluation Flow
# ==============================================================================
def generate_validation_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 6))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    ax.text(5.75, 5.65, "Nested Cross-Validation & Hyperparameter Optimization Workflow",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#0D233A")
    ax.text(5.75, 5.3, "Unbiased Performance Estimation and Automated Bayesian Search Structure",
            ha='center', va='center', fontsize=8.5, color="#555555", style='italic')

    # Main Dataset Split
    create_box(ax, 0.5, 2.2, 1.8, 2.2, "Complete Dataset", "Stratified Partition:\n• 80% Dev/Train Set\n• 20% Holdout Test\n(Never touched in CV)", color="#2C3E50")
    
    # Outer CV Loop
    create_box(ax, 2.9, 2.9, 2.4, 1.8, "Outer Loop: K=5 Folds", "Generalization Estimate:\n• Fold 1 to 5 Test splits\n• Out-of-Fold predictions\n• Variance & Stability Metric", color="#2980B9")
    
    # Inner CV Loop / Optuna
    create_box(ax, 5.8, 2.9, 2.5, 1.8, "Inner Loop: Optuna HPO", "Bayesian Optimization:\n• TPE Sampler (100 trials)\n• K=3 Inner Validation\n• Median Pruning of trials\n• Best params extraction", color="#E67E22")
    
    # Multi-Metric Evaluation Box
    create_box(ax, 8.8, 2.9, 2.2, 1.8, "Performance Metrics", "• PR-AUC & ROC-AUC\n• Cost-Benefit F2-Score\n• Brier Calibration Loss\n• Confusion Matrix Threshold", color="#27AE60")
    
    # Final Model Training
    create_box(ax, 5.8, 0.7, 2.5, 1.4, "Final Retrain on Full Dev", "Fit on all 80% Dev data\nusing optimal params", color="#8E44AD")
    
    # Final Holdout Test Verification
    create_box(ax, 8.8, 0.7, 2.2, 1.4, "Holdout Benchmark", "Unbiased validation test\nVerify generalization delta", color="#C0392B")

    # Arrows
    draw_arrow(ax, (2.3, 3.8), (2.9, 3.8), "80% Dev")
    draw_arrow(ax, (5.3, 3.8), (5.8, 3.8), "Train Folds")
    draw_arrow(ax, (8.3, 3.8), (8.8, 3.8), "Evaluate")
    draw_arrow(ax, (7.05, 2.9), (7.05, 2.1), "Optimal Params")
    draw_arrow(ax, (8.3, 1.4), (8.8, 1.4), "Predict")
    
    # Out of Time / Holdout arrow
    draw_arrow(ax, (1.4, 2.2), (1.4, 1.4), connectionstyle="arc3,rad=0.0")
    draw_arrow(ax, (1.4, 1.4), (8.8, 1.4), "20% Holdout Test", connectionstyle="arc3,rad=-0.1", label_offset=(0, 0.2))

    plt.tight_layout()
    path = os.path.join(output_dir, "validation_tuning_flow.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

# ==============================================================================
# Diagram 4: MLOps Deployment & Monitoring Lifecycle
# ==============================================================================
def generate_mlops_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 6.2))
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    
    ax.text(5.75, 6.1, "Production Deployment, Serving & Continuous Monitoring (MLOps)",
            ha='center', va='center', fontsize=13, fontweight='bold', color="#0D233A")
    ax.text(5.75, 5.75, "Robust High-Throughput Inference, Real-Time Drift Detection, and CI/CD/CT Automation",
            ha='center', va='center', fontsize=8.5, color="#555555", style='italic')

    # Registry & Packaging
    create_box(ax, 0.5, 3.6, 2.2, 1.5, "Model Registry & Artifacts", "• MLflow Model Registry\n• ONNX / Joblib format\n• Versioning & Metadata\n• Signature & Schemas", color="#2C3E50")

    # Serving Layer
    create_box(ax, 3.3, 3.6, 2.4, 1.5, "Serving & Inference", "• FastAPI Microservice\n• Docker Containerization\n• Real-Time REST (<25ms)\n• Batch Scoring Worker", color="#2980B9")

    # Client / Downstream Consumers
    create_box(ax, 6.3, 3.6, 2.2, 1.5, "Business Consumers", "• CRM Dashboard\n• Retention Campaign Ops\n• Automated Discounts\n• Churn Risk Alerts", color="#27AE60")

    # Observability & Monitoring
    create_box(ax, 3.3, 1.0, 2.4, 1.6, "Drift & Observability", "• Data Drift (KS-Test/PSI)\n• Concept Drift Tracking\n• Evidently AI / Prometheus\n• Latency & Error Logging", color="#D35400")

    # Automated CI/CD/CT Pipeline
    create_box(ax, 0.5, 1.0, 2.2, 1.6, "Automated CI/CD/CT", "• Retraining Trigger\n• Canary / Blue-Green Deploy\n• Auto-rollback on anomaly\n• GitHub Actions / Airflow", color="#8E44AD")

    # Arrows
    draw_arrow(ax, (2.7, 4.35), (3.3, 4.35), "Deploy")
    draw_arrow(ax, (5.7, 4.35), (6.3, 4.35), "Probabilities")
    draw_arrow(ax, (4.5, 3.6), (4.5, 2.6), "Inference Logs")
    draw_arrow(ax, (3.3, 1.8), (2.7, 1.8), "Drift Alert (>0.2 PSI)")
    draw_arrow(ax, (1.6, 2.6), (1.6, 3.6), "New Model Candidate")

    plt.tight_layout()
    path = os.path.join(output_dir, "mlops_deployment_lifecycle.png")
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

if __name__ == "__main__":
    generate_lifecycle_diagram()
    generate_preprocessing_diagram()
    generate_validation_diagram()
    generate_mlops_diagram()
    print("All 4 architectural diagrams successfully generated.")
