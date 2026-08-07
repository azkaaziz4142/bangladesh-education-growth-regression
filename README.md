# Impact of Education and Child Labor on Economic Growth in Bangladesh

Econometrics course project analyzing how illiteracy, child labor, and education
expenditure affect GDP per capita in Bangladesh (1988–2022), using a multiple
linear regression model.

**Author:** Azka Aziz

**Course:** Econometrics 

## Research Question

Do reductions in illiteracy and child labor significantly increase GDP per
capita in Bangladesh, and does education expenditure act as a growth driver?

- **H₁:** Reductions in illiteracy and child labor significantly increase GDP per capita.
- **H₀:** Reductions in illiteracy and child labor have no significant effect on GDP per capita.

## Model

```
ln_GDP_per_capita = β₀ + β₁(Illiteracy_rate) + β₂(Child_labour_rate) + β₃(Education_expenditure) + ε
```

## Data

File: [`data/Dataset.xlsx`](data/Dataset.xlsx) — annual panel, 1988–2022.

| Variable | Description | Source |
|---|---|---|
| `ln_GDP_per_capita` | Log of GDP per capita | World Bank (World Development Indicators) |
| `Illiteracy_rate` | % of population 15+ who are illiterate | UNESCO Institute for Statistics (via World Bank) |
| `Child_labour_rate` | % of children aged 5–17 in child labor | Bangladesh Bureau of Statistics (BBS) / ILO National Child Labour Survey |
| `Education_expenditure` | Government education spending, % of GDP | World Bank / UNESCO |

**Data notes:**
- `Illiteracy_rate` is genuine annual data, cross-checked against official World Bank/UNESCO figures.
- `Child_labour_rate` is based on the BBS/ILO National Child Labour Survey years (~2003, 2013, 2022, the only years Bangladesh actually surveys this); intermediate years were linearly interpolated to build a complete annual panel for the regression. This is disclosed here for transparency and reproducibility.

## Key Findings

- **Illiteracy rate**: statistically significant negative effect on GDP per capita (coefficient ≈ -0.0327).
- **Child labor rate**: not statistically significant in this model (coefficient ≈ 0.00585).
- **Education expenditure**: not statistically significant (coefficient ≈ -0.03246), suggesting its effect may be delayed or require more targeted investment.
- Model diagnostics (residuals vs. fitted, Q-Q, scale-location, leverage) support the model's core assumptions.

## Repository Structure

```
.
├── data/
│   └── bangladesh_gdp_dataset.xlsx     # Combined dataset used for the regression
├── presentation/
│   └── FA24-BBD-023-SEC-A.pptx         # Full project slide deck
├── scripts/
│   └── build_dataset.py                # Script to pull/rebuild the World Bank & UNESCO portions of the data
└── README.md
```

## Usage and Applications

This analysis is intended to inform:
- Government policy on education and child labor
- Economists and researchers studying growth drivers in South Asia
- NGOs and international organizations designing child welfare and education programs

## License

This project is shared for educational and portfolio purposes.
