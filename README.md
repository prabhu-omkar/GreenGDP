# Green GDP & Sustainable Development Analysis
### *Economics Subject Assignment & Research Workspace*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Data Source](https://img.shields.io/badge/Data-World%20Bank%20WDI-green.svg)](https://databank.worldbank.org/source/world-development-indicators)
[![Methodology](https://img.shields.io/badge/Methodology-UN%20SEEA%20Framework-orange.svg)](https://seea.un.org/)
[![Case Study](https://img.shields.io/badge/Featured%20Case%20Study-Bangladesh%20(BGD)-red.svg)](bangladesh_case_study/bangladesh.md)

---

## 📌 Executive Overview

Gross Domestic Product (GDP) under the standard **System of National Accounts (SNA)** measures total market value of goods and services produced within a country. However, conventional GDP suffers from a fundamental ecological blindness: **it treats natural capital depletion and environmental degradation either as zero-cost or as positive economic contributions**. 

This project implements an **Environmentally Adjusted Net Domestic Product (Green GDP)** framework to evaluate whether observed economic growth reflects genuine welfare expansion or illusory gains funded by environmental asset liquidation across 164 nations.

### Primary Objectives:
1. **Green GDP Computation**: Quantify Net Natural Capital Consumption (NNCC) across 164 countries from 2008 to 2018 using World Bank Open Data.
2. **Featured Case Study (Bangladesh)**: Dedicated in-depth evaluation of Bangladesh's transition from Low-Income to Lower-Middle-Income status against its climate vulnerability paradox.
3. **Decoupling Elasticity Analysis**: Determine whether economic growth has decoupled from $\text{CO}_2$ damage and particulate air pollution using OECD/Tapio elasticity models.
4. **Statistical & Predictive Modeling**: Compute Pearson correlation matrices and project economic/environmental trends through polynomial regression forecasting to 2030.

---

## 🇧🇩 Featured Case Study: Bangladesh

Our primary empirical research and assignment focus was conducted on **Bangladesh (BGD)**. 

All comprehensive case study materials, including the 10-year year-by-year dataset tables, high-resolution visualization charts, PowerPoint presentation, statistical models, and policy recommendations have been organized into a dedicated case study module:

👉 **[View Full Bangladesh Case Study Document (`bangladesh.md`)](bangladesh_case_study/bangladesh.md)**  
👉 **[View PowerPoint Presentation Deck (`Bangladesh.pptx`)](bangladesh_case_study/Bangladesh.pptx)**  
👉 **[Browse Case Study Visualizations & Assets (`bangladesh_case_study/`)](bangladesh_case_study/)**

---

## 🧮 Theoretical & Mathematical Framework

Green GDP is computed using the **United Nations System of Environmental-Economic Accounting (SEEA)** framework:

$$\text{Green GDP}_t = \text{GDP}_t - \text{NNCC}_t$$

Where **Net Natural Capital Consumption ($\text{NNCC}_t$)** is defined as the sum of non-renewable natural resource depletion and externalized environmental degradation:

$$\text{NNCC}_t = \text{Resource Depletion}_t + \text{Environmental Degradation}_t$$

### 1. Component Formulas

* **Resource Depletion ($\text{USD}$)**:
  $$\text{Resource Depletion}_t = \left( \frac{\text{NRD}_{\%, t}}{100} \right) \times \text{GNI}_t$$
  *where $\text{NRD}_{\%}$ is the sum of energy, mineral, and net forest depletion as a percentage of Gross National Income ($\text{GNI}$).*

* **Environmental Degradation ($\text{USD}$)**:
  $$\text{Environmental Degradation}_t = \text{CO}_2 \text{ Damage}_t + \text{Particulate Emission Damage (PED)}_t$$
  *where $\text{CO}_2 \text{ Damage}$ represents global social damage costs of carbon emissions, and $\text{PED}$ represents local health and economic burdens of $\text{PM}_{2.5}$ exposure.*

* **Green GDP Gap ($\%$)**:
  $$\text{Green GDP Gap}_t = \frac{\text{GDP}_t - \text{Green GDP}_t}{\text{GDP}_t} \times 100 = \frac{\text{NNCC}_t}{\text{GDP}_t} \times 100$$

* **Sustainability Index ($\text{SI}$)**:
  $$\text{Sustainability Index}_t = \frac{\text{Green GDP}_t}{\text{GDP}_t} \quad \left(0 \le \text{SI} \le 1.0; \text{ Higher is more sustainable}\right)$$

### 2. Decoupling Elasticity ($\varepsilon$)

To analyze the relationship between economic growth and environmental damage, we compute the OECD/Tapio elasticity of emissions/damage with respect to GDP growth:

$$\varepsilon = \frac{\% \, \Delta \, \text{Environmental Degradation}}{\% \, \Delta \, \text{GDP}} = \frac{(\text{EnvDeg}_t - \text{EnvDeg}_{t-1}) / \text{EnvDeg}_{t-1}}{(\text{GDP}_t - \text{GDP}_{t-1}) / \text{GDP}_{t-1}}$$

| Elasticity Range | Decoupling Regime | Economic Interpretation |
| :--- | :--- | :--- |
| **$\varepsilon < 0$** | **Absolute Decoupling** | Environmental damage decreases while GDP grows. *Ideal sustainable path.* |
| **$0 \le \varepsilon < 1$** | **Relative Decoupling** | Environmental damage increases, but at a slower rate than GDP growth. |
| **$\varepsilon \ge 1$** | **No Decoupling / Recoupling** | Environmental damage increases faster than or at the same rate as GDP growth. |

---

## 📂 Project Architecture

```
c:/projects/economics/
│
├── 📜 README.md                     # Main project guide & framework documentation
├── 🐍 green_gdp_analysis.py         # Main analysis pipeline (Data processing, CSV exports, plots)
├── 🐍 advanced_analytics.py         # Advanced stats (Decoupling elasticity, correlation, polynomial forecast)
│
├── 📁 bangladesh_case_study/        # 🇧🇩 Dedicated Case Study Folder
│   ├── 📜 bangladesh.md             # Detailed case study writeup & report
│   ├── 📊 Bangladesh.pptx           # PowerPoint presentation slides
│   └── 📁 output/                   # Generated case study images
│       ├── 🖼️ bangladesh_gdp_vs_green.png # Standard vs Green GDP chart
│       ├── 🖼️ bangladesh_nncc_breakdown.png # Resource & pollution cost breakdown
│       ├── 🖼️ bangladesh_gap_trend.png  # Green GDP Gap % over time
│       ├── 🖼️ bangladesh_pie.png        # Environmental cost share pie chart
│       ├── 🖼️ bangladesh_sustainability.png # Sustainability Index progression
│       ├── 🖼️ bangladesh_decoupling.png # Decoupling elasticity plot
│       ├── 🖼️ bangladesh_correlation_matrix.png # Statistical correlation heatmap
│       ├── 🖼️ bangladesh_forecast.png   # Polynomial regression forecast to 2023
│       ├── 🖼️ bangladesh_forecast_2030.png # Polynomial regression forecast to 2030
│       └── 🖼️ bangladesh_comparison.png # Benchmarking against peer nations
│
├── 📁 dataset/                      # Raw World Bank Development Indicators (2008-2018)
│   ├── country_gdp.csv              # NY.GDP.MKTP.CD - GDP (current US$)
│   ├── country_gni.csv              # NY.GNP.MKTP.CD - GNI (current US$)
│   ├── country_nrd.csv              # NY.ADJ.DRES.GN.ZS - Resource Depletion (% of GNI)
│   ├── country_co2.csv              # NY.ADJ.DCO2.CD - CO₂ Damage (current US$)
│   └── country_ped.csv              # NY.ADJ.DPEM.CD - Particulate Emission Damage (current US$)
│
├── 📁 output/                       # Output directory for general runs
└── 📁 global_result/                # Cross-country batch calculation results
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup

Ensure Python 3.8+ is installed. Install required data science packages:

```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 2. Running Green GDP Analysis

To run the primary pipeline for any country (set `COUNTRY_CODE` in script):

```bash
python -X utf8 green_gdp_analysis.py
```
*> Note: The `-X utf8` flag ensures proper UTF-8 character rendering in Windows environments.*

#### Configuring Target Country:
Open [`green_gdp_analysis.py`](green_gdp_analysis.py) and set line 22:
```python
COUNTRY_CODE = "BGD"  # ISO 3-letter country code (e.g., BGD, IND, VNM, PAK, CHN, DEU, USA)
```

### 3. Running Advanced Analytics & Forecasting

To run decoupling elasticity, correlation matrices, and 2nd-degree polynomial projections:

```bash
python -X utf8 advanced_analytics.py
```

---

## 🌎 Supported Countries (164 ISO Codes)

The repository supports automated analysis for 164 countries in the World Bank database. Examples include:

| Region | Country | ISO Code | Region | Country | ISO Code |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **South Asia** | Bangladesh | `BGD` | **East Asia** | China | `CHN` |
| | India | `IND` | | Vietnam | `VNM` |
| | Pakistan | `PAK` | | Indonesia | `IDN` |
| | Sri Lanka | `LKA` | | Philippines | `PHL` |
| **Europe** | Germany | `DEU` | **Americas** | United States | `USA` |
| | United Kingdom | `GBR` | | Brazil | `BRA` |
| | France | `FRA` | | Mexico | `MEX` |

---

## 📚 Academic References

* **United Nations et al. (2014)**. *System of Environmental-Economic Accounting 2012 — Central Framework*. New York: UN, EU, FAO, IMF, OECD, World Bank.
* **World Bank (2021)**. *The Changing Wealth of Nations 2021: Managing Assets for the Future*. Washington, DC: World Bank Group.
* **Nordhaus, W. D., & Tobin, J. (1972)**. *Is Growth Obsolete?* Economic Research: Retrospect and Prospect, Vol. 5: Economic Growth. NBER.
* **Pearce, D. W., & Atkinson, G. D. (1993)**. *Capital theory and the measurement of sustainable development: an indicator of "weak" sustainability*. Ecological Economics, 8(2), 103-108.
* **Tapio, P. (2005)**. *Towards a theory of decoupling: degrees of decoupling in the EU transport sector 1970–2001*. Transport Policy, 12(2), 137-151.

---

### 🎓 Assignment Details
* **Subject**: Economics (Environmental Economics & Macroeconomic Accounting)
* **Dataset**: World Bank World Development Indicators (WDI)
* **Case Study Module**: [`bangladesh_case_study/bangladesh.md`](bangladesh_case_study/bangladesh.md)
* **Primary Analysis Code**: [`green_gdp_analysis.py`](green_gdp_analysis.py)
* **Advanced Analytics Code**: [`advanced_analytics.py`](advanced_analytics.py)
         