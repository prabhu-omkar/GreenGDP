# Case Study: True Economic Progress of Bangladesh (2008–2018)
### *Green GDP & Sustainable Development Analysis*

[![Country](https://img.shields.io/badge/Country-Bangladesh%20(BGD)-red.svg)](bangladesh.md)
[![Data Source](https://img.shields.io/badge/Data-World%20Bank%20WDI-green.svg)](https://databank.worldbank.org/source/world-development-indicators)
[![Presentation](https://img.shields.io/badge/Presentation-Bangladesh.pptx-blue.svg)](Bangladesh.pptx)

---

## 📌 Executive Summary

This case study evaluates whether Bangladesh's rapid economic growth between 2008 and 2018 represents genuine improvements in national wellbeing or masks significant natural capital depletion and environmental degradation. By computing **Green GDP** — standard GDP minus the monetary value of natural resource depletion and pollution costs — we reveal the true cost of growth.

### Core Key Findings (2008–2018):

| Metric | Empirical Value | Economic Interpretation |
| :--- | :---: | :--- |
| **Standard GDP CAGR** | **13.37%** | Nominal expansion from $\$91.64\text{B}$ to $\$321.36\text{B}$ ($3.51\times$). |
| **Green GDP CAGR** | **13.52%** | Environmentally adjusted growth from $\$88.27\text{B}$ to $\$313.71\text{B}$ ($3.55\times$). |
| **Average Green GDP Gap** | **3.25%** | Percentage of annual economic output absorbed by natural capital costs. |
| **Average Sustainability Index** | **0.9675** | Ratio of Green GDP to Standard GDP ($1.00 = \text{perfect sustainability}$). |
| **10-Year Cumulative NNCC** | **$\$59.68 \text{ Billion}$** | Total monetary cost of resource depletion and environmental damage. |
| **$\text{CO}_2$ Decoupling Elasticity ($\varepsilon$)** | **1.127** | **No Decoupling (Recoupled)**: Emissions damage grew faster than GDP. |
| **Overall NNCC Elasticity ($\varepsilon$)** | **0.735** | **Relative Decoupling**: Aggregate environmental costs grew slower than GDP. |

**Verdict:** Bangladesh's economic growth is genuine and expanding national welfare. The Green GDP Gap declined from $3.67\%$ in 2008 to $2.38\%$ in 2018, indicating that environmental costs consume a shrinking share of national output. However, $\text{CO}_2$ damage remains tightly coupled to economic expansion ($\varepsilon > 1$), posing long-term climate vulnerabilities.

---

## 🇧🇩 Country Profile: Why Bangladesh?

1. **Rapid Structural Transformation**:
   Between 2008 and 2018, Bangladesh transitioned from a Low-Income Country (LIC) to a Lower-Middle-Income Country (LMIC) (World Bank, 2015). By 2018, its sector composition stood at:
   * **Services**: $\sim 53\%$ of GDP
   * **Industry**: $\sim 30\%$ of GDP (dominated by Ready-Made Garments - RMG, generating $\$30.6\text{B}$ in export revenue)
   * **Agriculture**: $\sim 13\%$ of GDP

2. **The Climate Vulnerability Paradox**:
   Bangladesh contributes less than $0.35\%$ of global greenhouse emissions but ranks among the top 10 most climate-vulnerable nations worldwide. Over $80\%$ of its landmass is floodplain, and projections suggest $17\%$ of territory could be lost to sea-level rise by 2050.

3. **Natural Resource Depletion Profile**:
   Bangladesh's primary non-renewable asset is natural gas, historically powering $\sim 62\%$ of domestic power generation. Domestic gas reserves face severe depletion, forcing an increasing reliance on expensive imported LNG.

---

## 🧮 Empirical Methodology & Formulations

$$\text{Green GDP} = \text{Standard GDP} - \text{Net Natural Capital Consumption (NNCC)}$$

$$\text{NNCC} = \text{Resource Depletion (USD)} + \text{CO}_2 \text{ Damage (USD)} + \text{Particulate Emission Damage (PED USD)}$$

### World Bank Indicators Applied:
* **GDP (current US$)**: `NY.GDP.MKTP.CD`
* **GNI (current US$)**: `NY.GNP.MKTP.CD`
* **Natural Resource Depletion (% of GNI)**: `NY.ADJ.DRES.GN.ZS`
* **$\text{CO}_2$ Damage (current US$)**: `NY.ADJ.DCO2.CD`
*