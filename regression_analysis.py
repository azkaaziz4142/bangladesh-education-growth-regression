"""
Impact of Education and Child Labor on Economic Growth in Bangladesh
Multiple linear regression + diagnostic plots.

Model:
    ln_GDP_per_capita = b0 + b1*Illiteracy_rate + b2*Child_labour_rate
                         + b3*Education_expenditure + e

Run:
    pip install pandas numpy matplotlib scipy openpyxl
    python regression_analysis.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

DATA_PATH = "data/bangladesh_gdp_dataset.xlsx"
OUT_DIR = "figures"

import os
os.makedirs(OUT_DIR, exist_ok=True)

# ---- Load data ----
df = pd.read_excel(DATA_PATH)

y = df["ln_GDP_per_capita"].values
X_vars = ["Illiteracy_rate", "Child_labour_rate", "Education_expenditure"]
X_raw = df[X_vars].values
n, k = X_raw.shape

# Design matrix with intercept
X = np.column_stack([np.ones(n), X_raw])

# ---- OLS via normal equations ----
XtX_inv = np.linalg.inv(X.T @ X)
beta = XtX_inv @ X.T @ y
y_hat = X @ beta
residuals = y - y_hat

dof = n - (k + 1)
rss = np.sum(residuals ** 2)
sigma2 = rss / dof
se_beta = np.sqrt(np.diag(sigma2 * XtX_inv))
t_stats = beta / se_beta
p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), dof))

tss = np.sum((y - y.mean()) ** 2)
r_squared = 1 - rss / tss
adj_r_squared = 1 - (1 - r_squared) * (n - 1) / dof

# ---- Print summary table ----
labels = ["Intercept"] + X_vars
print("=" * 70)
print("OLS Regression Results")
print("=" * 70)
print(f"{'Variable':<24}{'Coef':>10}{'Std Err':>12}{'t':>10}{'P>|t|':>10}")
for label, b, se, t, p in zip(labels, beta, se_beta, t_stats, p_values):
    print(f"{label:<24}{b:>10.5f}{se:>12.5f}{t:>10.3f}{p:>10.4f}")
print("-" * 70)
print(f"N = {n}   R-squared = {r_squared:.4f}   Adj. R-squared = {adj_r_squared:.4f}")
print("=" * 70)

# ---- Diagnostic plots (matches the 4-panel layout used in the slides) ----
leverage = np.diag(X @ XtX_inv @ X.T)
std_residuals = residuals / (np.sqrt(sigma2) * np.sqrt(1 - leverage))

fig, axes = plt.subplots(2, 2, figsize=(11, 9))

# 1. Residuals vs Fitted
axes[0, 0].scatter(y_hat, residuals, edgecolor="k", facecolor="none")
axes[0, 0].axhline(0, color="red", linestyle="--", linewidth=1)
axes[0, 0].set_xlabel("Fitted values")
axes[0, 0].set_ylabel("Residuals")
axes[0, 0].set_title("Residuals vs Fitted")

# 2. Normal Q-Q
stats.probplot(std_residuals, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title("Normal Q-Q")

# 3. Scale-Location
sqrt_std_resid = np.sqrt(np.abs(std_residuals))
axes[1, 0].scatter(y_hat, sqrt_std_resid, edgecolor="k", facecolor="none")
axes[1, 0].set_xlabel("Fitted values")
axes[1, 0].set_ylabel("sqrt(|Standardized residuals|)")
axes[1, 0].set_title("Scale-Location")

# 4. Residuals vs Leverage (with Cook's distance contours)
cooks_d = (std_residuals ** 2 / (k + 1)) * (leverage / (1 - leverage))
axes[1, 1].scatter(leverage, std_residuals, edgecolor="k", facecolor="none")
axes[1, 1].axhline(0, color="grey", linewidth=0.8)
axes[1, 1].set_xlabel("Leverage")
axes[1, 1].set_ylabel("Standardized residuals")
axes[1, 1].set_title("Residuals vs Leverage")

plt.tight_layout()
plt.savefig(f"{OUT_DIR}/diagnostic_plots.png", dpi=150)
print(f"\nSaved diagnostic plots to {OUT_DIR}/diagnostic_plots.png")

# ---- Save regression summary to a text file ----
with open(f"{OUT_DIR}/regression_summary.txt", "w") as f:
    f.write("OLS Regression Results\n")
    f.write("Dependent variable: ln_GDP_per_capita\n\n")
    f.write(f"{'Variable':<24}{'Coef':>10}{'Std Err':>12}{'t':>10}{'P>|t|':>10}\n")
    for label, b, se, t, p in zip(labels, beta, se_beta, t_stats, p_values):
        f.write(f"{label:<24}{b:>10.5f}{se:>12.5f}{t:>10.3f}{p:>10.4f}\n")
    f.write(f"\nN = {n}   R-squared = {r_squared:.4f}   Adj. R-squared = {adj_r_squared:.4f}\n")
print(f"Saved regression summary to {OUT_DIR}/regression_summary.txt")
