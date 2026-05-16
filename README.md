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
| **$0 \le \varepsilon < 1$** | **Relative Decoupling** | Environmental damage increases, but at a slower rate than GDP g