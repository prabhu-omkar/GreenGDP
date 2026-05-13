"""
Green GDP Comprehensive Analysis — Bangladesh (BGD)
=====================================================
Combined analysis: Core Green GDP calculation, advanced analytics,
decoupling elasticity, correlation matrix, and polynomial forecasting to 2030.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os, warnings, sys

warnings.filterwarnings("ignore")

# ╔══════════════════════════════════════════════════════════════╗
# ║  CONFIGURATION                                               ║
# ╚══════════════════════════════════════════════════════════════╝
COUNTRY_CODE = "BGD"
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
YEARS = [str(y) for y in range(2008, 2019)]
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
DATASET_DIR = os.path.join(DATA_DIR, "dataset")

FILES = {
    "gdp": os.path.join(DATASET_DIR, "country_gdp.csv"),
    "gni": os.path.join(DATASET_DIR, "country_gni.csv"),
    "nrd": os.path.join(DATASET_DIR, "country_nrd.csv"),
    "co2": os.path.join(DATASET_DIR, "country_co2.csv"),
    "ped": os.path.join(DATASET_DIR, "country_ped.csv"),
}

# ─── Helpers ─────────────────────────────────────────────────
def load_wb_csv(filepath, years):
    df = pd.read_csv(filepath, skiprows=4, encoding="utf-8-sig")
    keep = ["Country Name", "Country Code"] + [y for y in years if y in df.columns]
    df = df[keep].copy()
    for y in years:
        if y in df.columns:
            df[y] = pd.to_numeric(df[y], errors="coerce")
    return df

def to_long(df, val_name, years):
    ycols = [y for y in years if y in df.columns]
    m = df.melt(id_vars=["Country Name", "Country Code"], value_vars=ycols,
                var_name="Year", value_name=val_name)
    m["Year"] = m["Year"].astype(int)
    return m

def fmt_b(val):
    return f"${val/1e9:.2f}B"

# ─── Main ────────────────────────────────────────────────────
def main():
    code = COUNTRY_CODE.upper()

    # ═══════════════════════════════════════════════════════════
    # SECTION 1: DATA LOADING & GREEN GDP CALCULATION
    # ═══════════════════════════════════════════════════════════
    gdp = load_wb_csv(FILES["gdp"], YEARS)
    gni = load_wb_csv(FILES["gni"], YEARS)
    nrd = load_wb_csv(FILES["nrd"], YEARS)
    co2 = load_wb_csv(FILES["co2"], YEARS)
    ped = load_wb_csv(FILES["ped"], YEARS)

    mg = to_long(gdp, "GDP", YEARS)
    mg = mg.merge(to_long(gni, "GNI", YEARS)[["Country Code","Year","GNI"]], on=["Country Code","Year"])
    mg = mg.merge(to_long(nrd, "NRD_PCT", YEARS)[["Country Code","Year","NRD_PCT"]], on=["Country Code","Year"])
    mg = mg.merge(to_long(co2, "CO2_DMG", YEARS)[["Country Code","Year","CO2_DMG"]], on=["Country Code","Year"])
    mg = mg.merge(to_long(ped, "PED", YEARS)[["Country Code","Year","PED"]], on=["Country Code","Year"])

    # Core calculations
    mg["Res_Depl"] = (mg["NRD_PCT"] / 100) * mg["GNI"]
    mg["Env_Deg"] = mg["CO2_DMG"] + mg["PED"]
    mg["NNCC"] = mg["Res_Depl"] + mg["Env_Deg"]
    mg["Green_GDP"] = mg["GDP"] - mg["NNCC"]
    mg["Gap_Pct"] = (mg["GDP"] - mg["Green_GDP"]) / mg["GDP"] * 100
    mg["Sust_Idx"] = mg["Green_GDP"] / mg["GDP"]

    # Filter country
    c = mg[mg["Country Code"] == code].dropna(subset=["GDP","Green_GDP"]).sort_values("Year").reset_index(drop=True)
    if c.empty:
        print(f"ERROR: No data found for country code '{code}'.")
        return

    name = c.iloc[0]["Country Name"]
    tag = name.lower().replace(" ", "_").replace(",", "")

    # ═══════════════════════════════════════════════════════════
    # SECTION 2: CONSOLE OUTPUT
    # ═══════════════════════════════════════════════════════════
    print("=" * 100)
    print(f"  COMPREHENSIVE GREEN GDP ANALYSIS: {name.upper()} ({code}) | 2008-2018")
    print("=" * 100)

    print(f"\n{'Year':<6} {'Std GDP':>13} {'Green GDP':>13} {'Res Depl':>13} {'CO2 Dmg':>13} {'PED':>10} {'NNCC':>13} {'Gap%':>7} {'Sust Idx':>9}")
    print("-" * 100)
    for _, r in c.iterrows():
        print(f"{int(r['Year']):<6} {fmt_b(r['GDP']):>13} {fmt_b(r['Green_GDP']):>13} "
              f"{fmt_b(r['Res_Depl']):>13} {fmt_b(r['CO2_DMG']):>13} {fmt_b(r['PED']):>10} "
              f"{fmt_b(r['NNCC']):>13} {r['Gap_Pct']:>6.2f}% {r['Sust_Idx']:>8.4f}")
    print("-" * 100)

    # CAGR
    n = len(c) - 1
    gdp_cagr = ((c.iloc[-1]["GDP"] / c.iloc[0]["GDP"]) ** (1/n) - 1) * 100
    ggdp_cagr = ((c.iloc[-1]["Green_GDP"] / c.iloc[0]["Green_GDP"]) ** (1/n) - 1) * 100
    nncc_cagr = ((c.iloc[-1]["NNCC"] / c.iloc[0]["NNCC"]) ** (1/n) - 1) * 100
    co2_cagr = ((c.iloc[-1]["CO2_DMG"] / c.iloc[0]["CO2_DMG"]) ** (1/n) - 1) * 100
    res_cagr = ((c.iloc[-1]["Res_Depl"] / c.iloc[0]["Res_Depl"]) ** (1/n) - 1) * 100
    ped_cagr = ((c.iloc[-1]["PED"] / c.iloc[0]["PED"]) ** (1/n) - 1) * 100

    print(f"\n  -- Growth Rates (CAGR 2008-2018) --")
    print(f"  Standard GDP CAGR:       {gdp_cagr:.2f}%")
    print(f"  Green GDP CAGR:          {ggdp_cagr:.2f}%")
    print(f"  NNCC CAGR:               {nncc_cagr:.2f}%")
    print(f"  CO2 Damage CAGR:         {co2_cagr:.2f}%")
    print(f"  Resource Depletion CAGR: {res_cagr:.2f}%")
    print(f"  PED CAGR:                {ped_cagr:.2f}%")
    print(f"\n  Avg Green GDP Gap:       {c['Gap_Pct'].mean():.2f}%")
    print(f"  Avg Sustainability Idx:  {c['Sust_Idx'].mean():.4f}")
    print(f"  Total NNCC (cumulative): {fmt_b(c['NNCC'].sum())}")
    print(f"  GDP Multiplier (10yr):   {c.iloc[-1]['GDP'] / c.iloc[0]['GDP']:.2f}x")
    print(f"  NNCC Multiplier (10yr):  {c.iloc[-1]['NNCC'] / c.iloc[0]['NNCC']:.2f}x")

    # ═══════════════════════════════════════════════════════════
    # SECTION 3: DECOUPLING / ELASTICITY ANALYSIS
    # ═══════════════════════════════════════════════════════════
    c['GDP_Growth'] = c['GDP'].pct_change()
    c['CO2_Growth'] = c['CO2_DMG'].pct_change()
    c['EnvDeg_Growth'] = c['Env_Deg'].pct_change()
    c['NNCC_Growth'] = c['NNCC'].pct_change()
    c['Res_Growth'] = c['Res_Depl'].pct_change()
    c['PED_Growth'] = c['PED'].pct_change()

    c['CO2_Elasticity'] = c['CO2_Growth'] / c['GDP_Growth']
    c['EnvDeg_Elasticity'] = c['EnvDeg_Growth'] / c['GDP_Growth']
    c['NNCC_Elasticity'] = c['NNCC_Growth'] / c['GDP_Growth']

    avg_co2_e = c['CO2_Elasticity'].dropna().mean()
    avg_env_e = c['EnvDeg_Elasticity'].dropna().mean()
    avg_nncc_e = c['NNCC_Elasticity'].dropna().mean()

    print(f"\n  -- Decoupling Analysis (Elasticity) --")
    print(f"  CO2 Damage / GDP Elasticity:    {avg_co2_e:.3f}")
    print(f"  Env Degradation / GDP Elasticity: {avg_env_e:.3f}")
    print(f"  NNCC / GDP Elasticity:           {avg_nncc_e:.3f}")

    for label, val in [("CO2", avg_co2_e), ("Env Degradation", avg_env_e), ("NNCC", avg_nncc_e)]:
        if val < 0:
            status = "ABSOLUTE DECOUPLING"
        elif val < 0.8:
            status = "STRONG RELATIVE DECOUPLING"
        elif val < 1.0:
            status = "WEAK RELATIVE DECOUPLING"
        else:
            status = "NO DECOUPLING (coupled growth)"
        print(f"    {label}: {status}")

    # ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    main()
