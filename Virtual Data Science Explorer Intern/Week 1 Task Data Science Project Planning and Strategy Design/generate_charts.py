import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates
import numpy as np

# Create figures directory
os.makedirs("figures", exist_ok=True)

# Set common style parameters
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8

# ==========================================
# 1. LIFECYCLE & PIPELINE FLOWCHART
# ==========================================
def generate_lifecycle_flowchart():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, "Project RetainAI: End-to-End Data Science Lifecycle & Pipeline Architecture", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
    ax.text(7, 7.15, "Iterative CRISP-DM Extended Framework with MLOps & Continuous Feedback Loops", 
            ha='center', va='center', fontsize=10, color='#475569', style='italic')

    # Stages definition
    stages = [
        {"title": "1. Ingestion & Specs", "sub": "Raw Data Sources\nValidation & Schemas\n(PostgreSQL / S3)", "x": 1.2, "y": 4.8, "color": "#e0f2fe", "border": "#0284c7"},
        {"title": "2. Prep & Cleaning", "sub": "Missing Handling\nOutlier Capping\nData Quality Checks", "x": 3.6, "y": 4.8, "color": "#e0e7ff", "border": "#4f46e5"},
        {"title": "3. EDA & Insights", "sub": "Cohort Analysis\nChurn Profiling\nMultivariate Corrs", "x": 6.0, "y": 4.8, "color": "#fef3c7", "border": "#d97706"},
        {"title": "4. Feature Store", "sub": "RFM Aggregations\nTemporal Lags\nNLP Sentiment Signals", "x": 8.4, "y": 4.8, "color": "#dcfce7", "border": "#16a34a"},
        {"title": "5. Modeling & Tuning", "sub": "XGBoost / LightGBM\nOptuna Tuning\nCost-Matrix Evaluator", "x": 10.8, "y": 4.8, "color": "#fae8ff", "border": "#9333ea"},
        {"title": "6. MLOps & Delivery", "sub": "FastAPI Microservice\nSHAP Explanations\nDrift Monitoring", "x": 13.0, "y": 4.8, "color": "#ffe4e6", "border": "#e11d48"}
    ]

    # Draw Stage Cards
    for stg in stages:
        box = patches.FancyBboxPatch(
            (stg["x"] - 0.95, stg["y"] - 1.2), 1.9, 2.4,
            boxstyle="round,pad=0.1,rounding_size=0.15",
            facecolor=stg["color"], edgecolor=stg["border"], linewidth=1.5, zorder=2
        )
        ax.add_patch(box)
        ax.text(stg["x"], stg["y"] + 0.8, stg["title"], ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a', zorder=3)
        ax.text(stg["x"], stg["y"] - 0.2, stg["sub"], ha='center', va='center', fontsize=8, color='#334155', linespacing=1.4, zorder=3)

    # Draw Horizontal Forward Arrows between stages
    for i in range(len(stages) - 1):
        x_start = stages[i]["x"] + 0.95
        x_end = stages[i+1]["x"] - 0.95
        y_pos = stages[i]["y"]
        ax.annotate('', xy=(x_end, y_pos), xytext=(x_start, y_pos),
                    arrowprops=dict(arrowstyle="-|>", color="#334155", lw=2, mutation_scale=15), zorder=4)

    # Feedback Loops / Iteration Paths
    # Modeling -> Feature Store feedback loop
    ax.annotate('Feature Refinement Loop', xy=(8.4, 3.4), xytext=(10.8, 3.4),
                arrowprops=dict(arrowstyle="-|>", color="#9333ea", lw=1.5, ls="--",
                                connectionstyle="arc3,rad=0.3", mutation_scale=12),
                ha='center', va='top', fontsize=8, color='#9333ea', fontweight='semibold')
    
    # MLOps Monitoring -> Ingestion Retraining feedback loop
    ax.annotate('Data Drift Trigger / Automated Model Retraining Pipeline', 
                xy=(1.2, 3.2), xytext=(13.0, 3.2),
                arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=1.8, ls="--",
                                connectionstyle="arc3,rad=0.25", mutation_scale=14),
                ha='center', va='top', fontsize=9, color='#be123c', fontweight='bold')

    # Bottom Foundation Bar: Governance, Tracking, Testing
    found_box = patches.FancyBboxPatch(
        (0.25, 0.4), 13.5, 1.4,
        boxstyle="round,pad=0.1,rounding_size=0.15",
        facecolor="#f1f5f9", edgecolor="#64748b", linewidth=1.2, linestyle=':', zorder=1
    )
    ax.add_patch(found_box)
    ax.text(7.0, 1.45, "FOUNDATIONAL GOVERNANCE & ENGINEERING PRACTICES", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.text(7.0, 0.85, "• Version Control (Git)  • Experiment Tracking (MLflow)  • Unit & Data Testing (PyTest / Great Expectations)  • CI/CD Pipeline & Reproducibility",
            ha='center', va='center', fontsize=8.5, color='#475569')

    plt.tight_layout()
    fig.savefig("figures/figure1_lifecycle_flowchart.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated figure 1: Lifecycle Flowchart")

# ==========================================
# 2. 30-35 HOUR GANTT TIMELINE CHART
# ==========================================
def generate_gantt_chart():
    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    tasks = [
        {"name": "Phase 1: Project Scoping & Data Architecture Specs", "start": 0, "duration": 5.0, "hours": "5.0 hrs", "color": "#0284c7"},
        {"name": "Phase 2: Data Preprocessing, Cleaning & Pipeline Design", "start": 5.0, "duration": 6.5, "hours": "6.5 hrs", "color": "#4f46e5"},
        {"name": "Phase 3: Exploratory Data Analysis & Feature Engineering Strategy", "start": 11.5, "duration": 7.0, "hours": "7.0 hrs", "color": "#d97706"},
        {"name": "Phase 4: ML Modeling, Hyperparameter Tuning & Evaluation Matrix", "start": 18.5, "duration": 8.0, "hours": "8.0 hrs", "color": "#16a34a"},
        {"name": "Phase 5: MLOps Architecture, Explainability & Final Documentation", "start": 26.5, "duration": 6.5, "hours": "6.5 hrs", "color": "#9333ea"}
    ]

    y_pos = np.arange(len(tasks))
    
    # Draw bars
    for i, t in enumerate(tasks):
        bar = ax.barh(y_pos[i], t["duration"], left=t["start"], height=0.55, 
                     color=t["color"], alpha=0.9, edgecolor='#1e293b', linewidth=0.8, zorder=3)
        # Add hours label inside/beside bar
        ax.text(t["start"] + t["duration"]/2, y_pos[i], f"{t['hours']}", 
                ha='center', va='center', color='#ffffff', fontweight='bold', fontsize=9, zorder=4)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([t["name"] for t in tasks], fontsize=9.5, fontweight='bold', color='#1e293b')
    ax.invert_yaxis()  # Top down

    # Milestones dashed vertical lines
    milestones = [
        {"x": 5.0, "label": "M1: PRD & Schema Spec Approved"},
        {"x": 11.5, "label": "M2: Clean Data Pipeline Verified"},
        {"x": 18.5, "label": "M3: Feature Store & Baseline Ready"},
        {"x": 26.5, "label": "M4: Champion ML Model Selected"},
        {"x": 33.0, "label": "M5: Strategy Doc & Prototype Complete"}
    ]

    for ms in milestones:
        ax.axvline(x=ms["x"], color='#94a3b8', linestyle='--', linewidth=1.2, zorder=2)
        ax.text(ms["x"], 4.8, ms["label"], rotation=45, ha='right', va='bottom', fontsize=8, color='#475569', fontweight='semibold')

    ax.set_xlabel("Cumulative Allocated Working Hours (Total = 33.0 Hours | Target Range: 30 - 35 Hours)", fontsize=10, fontweight='bold', color='#0f172a', labelpad=10)
    ax.set_xlim(0, 36)
    ax.set_xticks(range(0, 37, 3))
    ax.grid(axis='x', linestyle=':', color='#cbd5e1', alpha=0.7, zorder=1)

    ax.set_title("Project RetainAI: 30-35 Hour Work Breakdown Structure (WBS) & Timeline", 
                 fontsize=13, fontweight='bold', color='#0f172a', pad=15)
    
    # Sub-task breakdown summary box
    summary_text = (
        "Weekly Effort Allocation Summary (Total: 33.0 Hours):\n"
        "• Day 1-2 (Phase 1): Problem statement, stakeholder mapping, KPI definitions, schema contracts (5.0h)\n"
        "• Day 3-4 (Phase 2): Missing value imputation rules, outlier handling, automated Great Expectations suite (6.5h)\n"
        "• Day 5-6 (Phase 3): RFM modeling, cohort curves, temporal windowing, NLP sentiment signals (7.0h)\n"
        "• Day 7-8 (Phase 4): XGBoost/LightGBM benchmarks, Optuna hyperparameter optimization, Cost-Utility matrix (8.0h)\n"
        "• Day 9-10 (Phase 5): FastAPI specs, SHAP waterfall integration, drift triggers & executive deliverable compilation (6.5h)"
    )
    plt.figtext(0.12, -0.08, summary_text, fontsize=8, color='#334155', 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", edgecolor="#cbd5e1"))

    plt.tight_layout()
    fig.savefig("figures/figure2_project_gantt_timeline.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated figure 2: Gantt Timeline")

# ==========================================
# 3. SYSTEM ARCHITECTURE & SERVING BLUEPRINT
# ==========================================
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8fafc')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    ax.text(7, 8.1, "Project RetainAI: Multi-Tier Production System & Serving Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0f172a')

    # Columns / Layers
    layers = [
        {"title": "DATA SOURCES", "x": 1.5, "w": 2.2, "color": "#f1f5f9", "border": "#64748b",
         "items": ["PostgreSQL DB\n(User Subscriptions)", "Clickstream Logs\n(Segment / Kafka)", "Customer Tickets\n(Zendesk API / NLP)"]},
        {"title": "DATA & FEATURE ENGINE", "x": 4.5, "w": 2.4, "color": "#e0f2fe", "border": "#0284c7",
         "items": ["Polars / Pandas\nCleaning Pipeline", "Feast Feature Store\n(Batch + Streaming)", "Great Expectations\nSchema Validation"]},
        {"title": "MODELING & MLOps", "x": 7.7, "w": 2.4, "color": "#fae8ff", "border": "#9333ea",
         "items": ["XGBoost / LightGBM\nClassifier Models", "MLflow Registry\n& Versioning", "Optuna HPO &\nExplainability (SHAP)"]},
        {"title": "SERVING & ACTION LAYER", "x": 11.2, "w": 2.8, "color": "#dcfce7", "border": "#16a34a",
         "items": ["FastAPI REST Microservice\n(/predict_churn endpoint)", "Streamlit Operations\nRetention Dashboard", "Automated CRM Triggers\n(Discount & Outreach)"]}
    ]

    for col in layers:
        # Layer Header Box
        header_box = patches.FancyBboxPatch(
            (col["x"] - col["w"]/2, 6.8), col["w"], 0.6,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            facecolor=col["border"], edgecolor=col["border"], zorder=3
        )
        ax.add_patch(header_box)
        ax.text(col["x"], 7.1, col["title"], ha='center', va='center', fontsize=9, fontweight='bold', color='#ffffff', zorder=4)

        # Layer Container Box
        container = patches.FancyBboxPatch(
            (col["x"] - col["w"]/2, 1.8), col["w"], 4.8,
            boxstyle="round,pad=0.05,rounding_size=0.1",
            facecolor=col["color"], edgecolor=col["border"], linewidth=1.2, zorder=2
        )
        ax.add_patch(container)

        # Draw component cards inside
        y_offsets = [5.4, 3.8, 2.2]
        for y_off, item_text in zip(y_offsets, col["items"]):
            card = patches.FancyBboxPatch(
                (col["x"] - col["w"]/2 + 0.15, y_off), col["w"] - 0.3, 1.1,
                boxstyle="round,pad=0.05,rounding_size=0.08",
                facecolor="#ffffff", edgecolor="#cbd5e1", linewidth=1, zorder=3
            )
            ax.add_patch(card)
            ax.text(col["x"], y_off + 0.55, item_text, ha='center', va='center', fontsize=8, color='#1e293b', fontweight='medium', linespacing=1.3, zorder=4)

    # Inter-layer connecting arrows
    for x_s, x_e in [(2.6, 3.3), (5.7, 6.5), (8.9, 9.8)]:
        for y_pos in [5.95, 4.35, 2.75]:
            ax.annotate('', xy=(x_e, y_pos), xytext=(x_s, y_pos),
                        arrowprops=dict(arrowstyle="-|>", color="#475569", lw=1.5, mutation_scale=12), zorder=5)

    # Monitoring & Feedback Bar at bottom
    mon_box = patches.FancyBboxPatch(
        (0.4, 0.4), 13.2, 1.0,
        boxstyle="round,pad=0.05,rounding_size=0.1",
        facecolor="#ffe4e6", edgecolor="#e11d48", linewidth=1.2, zorder=2
    )
    ax.add_patch(mon_box)
    ax.text(7.0, 1.05, "CONTINUOUS OBSERVABILITY & GOVERNANCE LAYER (Evidently AI + Prometheus)", 
            ha='center', va='center', fontsize=9, fontweight='bold', color='#be123c')
    ax.text(7.0, 0.65, "Monitors Data Drift (KS-Test / PSI) • Concept Drift • Latency & Error Tracking • Automated Retraining Trigger Alert", 
            ha='center', va='center', fontsize=8, color='#4c0519')

    plt.tight_layout()
    fig.savefig("figures/figure3_system_architecture.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated figure 3: System Architecture")

# ==========================================
# 4. RISK IMPACT VS PROBABILITY MATRIX
# ==========================================
def generate_risk_matrix():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

    # Color zones
    colors = [
        ['#dcfce7', '#fef9c3', '#fed7aa'],  # Low prob: Low, Med, High impact
        ['#fef9c3', '#fed7aa', '#fecaca'],  # Med prob
        ['#fed7aa', '#fecaca', '#fda4af']   # High prob
    ]

    for y in range(3):
        for x in range(3):
            rect = patches.Rectangle((x, y), 1, 1, facecolor=colors[y][x], edgecolor='#cbd5e1', linewidth=1.2)
            ax.add_patch(rect)

    # Risk points
    risks = [
        {"code": "R1", "name": "Data Leakage across Temporal Windows", "x": 0.35, "y": 2.65, "bg": "#991b1b", "fg": "#ffffff"},
        {"code": "R2", "name": "Target Class Imbalance (Skewed Churn)", "x": 1.45, "y": 2.45, "bg": "#991b1b", "fg": "#ffffff"},
        {"code": "R3", "name": "Concept & Covariate Data Drift in Prod", "x": 1.5, "y": 1.4, "bg": "#c2410c", "fg": "#ffffff"},
        {"code": "R4", "name": "Inference Latency Spikes in REST API", "x": 2.5, "y": 0.45, "bg": "#854d0e", "fg": "#ffffff"},
        {"code": "R5", "name": "Disparate Impact & Retention Bias", "x": 0.45, "y": 1.35, "bg": "#854d0e", "fg": "#ffffff"},
        {"code": "R6", "name": "Stakeholder Resistance to Black-box ML", "x": 0.5, "y": 0.5, "bg": "#166534", "fg": "#ffffff"}
    ]

    for r in risks:
        circle = patches.Circle((r["x"], r["y"]), 0.12, facecolor=r["bg"], edgecolor='#ffffff', linewidth=1.5, zorder=4)
        ax.add_patch(circle)
        ax.text(r["x"], r["y"], r["code"], ha='center', va='center', fontsize=8.5, fontweight='bold', color=r["fg"], zorder=5)
        ax.text(r["x"] + 0.16, r["y"], r["name"], ha='left', va='center', fontsize=8, fontweight='semibold', color='#0f172a', zorder=5)

    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(['Low Impact', 'Medium Impact', 'High Impact'], fontsize=10, fontweight='bold', color='#1e293b')
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(['Low Probability', 'Medium Probability', 'High Probability'], fontsize=10, fontweight='bold', color='#1e293b')

    ax.set_xlabel("Impact Severity on Business & Model Quality", fontsize=10, fontweight='bold', color='#0f172a', labelpad=8)
    ax.set_ylabel("Occurrence Likelihood / Probability", fontsize=10, fontweight='bold', color='#0f172a', labelpad=8)
    ax.set_title("Project RetainAI: Strategic Risk Assessment & Mitigation Matrix", 
                 fontsize=12, fontweight='bold', color='#0f172a', pad=12)

    plt.tight_layout()
    fig.savefig("figures/figure4_risk_matrix.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated figure 4: Risk Matrix")

if __name__ == "__main__":
    generate_lifecycle_flowchart()
    generate_gantt_chart()
    generate_system_architecture()
    generate_risk_matrix()
    print("All diagrams generated successfully.")
