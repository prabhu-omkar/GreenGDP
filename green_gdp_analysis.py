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
    # SECTION 4: POLYNOMIAL FORECASTING TO 2030
    # ═══════════════════════════════════════════════════════════
    X = c['Year'].values
    y_gdp = c['GDP'].values
    y_green = c['Green_GDP'].values
    y_nncc = c['NNCC'].values
    y_co2 = c['CO2_DMG'].values
    y_res = c['Res_Depl'].values

    p_gdp = np.polyfit(X, y_gdp, 2)
    p_green = np.polyfit(X, y_green, 2)
    p_nncc = np.polyfit(X, y_nncc, 2)
    p_co2 = np.polyfit(X, y_co2, 2)

    years_all = np.array(range(2008, 2031))
    pred_gdp = np.polyval(p_gdp, years_all)
    pred_green = np.polyval(p_green, years_all)
    pred_nncc = np.polyval(p_nncc, years_all)
    pred_co2 = np.polyval(p_co2, years_all)

    print(f"\n  -- Polynomial Forecast (Degree 2) to 2030 --")
    print(f"  {'Year':<6} {'Proj GDP':>14} {'Proj Green GDP':>16} {'Proj NNCC':>14} {'Proj Gap%':>10}")
    print(f"  {'-'*62}")
    for i, yr in enumerate(years_all):
        gap = ((pred_gdp[i] - pred_green[i]) / pred_gdp[i] * 100) if pred_gdp[i] > 0 else 0
        marker = " *" if yr > 2018 else ""
        print(f"  {yr:<6} ${pred_gdp[i]/1e9:>12.2f}B ${pred_green[i]/1e9:>14.2f}B ${pred_nncc[i]/1e9:>12.2f}B {gap:>8.2f}%{marker}")

    # ═══════════════════════════════════════════════════════════
    # SECTION 5: CHARTS (9 total)
    # ═══════════════════════════════════════════════════════════
    plt.style.use("seaborn-v0_8-darkgrid")
    B = 1e9

    # ── Chart 1: GDP vs Green GDP ──
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(c["Year"], c["GDP"]/B, "o-", lw=2.5, color="#2196F3", ms=8, label="Standard GDP")
    ax.plot(c["Year"], c["Green_GDP"]/B, "s-", lw=2.5, color="#4CAF50", ms=8, label="Green GDP")
    ax.fill_between(c["Year"], c["Green_GDP"]/B, c["GDP"]/B, alpha=0.15, color="#F44336", label="Environmental Cost (NNCC)")
    ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("Billion USD", fontsize=12)
    ax.set_title(f"{name}: Standard GDP vs Green GDP (2008-2018)", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11); ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_gdp_vs_green.png"), dpi=150); plt.close()
    print(f"\n  [1/9] Saved: {tag}_gdp_vs_green.png")

    # ── Chart 2: Stacked bar NNCC breakdown ──
    fig, ax = plt.subplots(figsize=(12, 6))
    w = 0.6
    ax.bar(c["Year"], c["Res_Depl"]/B, w, label="Resource Depletion (NRD)", color="#FF9800")
    ax.bar(c["Year"], c["CO2_DMG"]/B, w, bottom=c["Res_Depl"]/B, label="CO₂ Damage", color="#F44336")
    ax.bar(c["Year"], c["PED"]/B, w, bottom=(c["Res_Depl"]+c["CO2_DMG"])/B, label="Particulate Emission Damage", color="#9C27B0")
    ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("Billion USD", fontsize=12)
    ax.set_title(f"{name}: Net Natural Capital Consumption Breakdown (2008-2018)", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11); ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_nncc_breakdown.png"), dpi=150); plt.close()
    print(f"  [2/9] Saved: {tag}_nncc_breakdown.png")

    # ── Chart 3: Green GDP Gap trend ──
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(c["Year"], c["Gap_Pct"], "D-", lw=2.5, color="#E91E63", ms=9)
    ax.fill_between(c["Year"], c["Gap_Pct"], alpha=0.2, color="#E91E63")
    for _, r in c.iterrows():
        ax.annotate(f"{r['Gap_Pct']:.2f}%", (r['Year'], r['Gap_Pct']),
                     textcoords="offset points", xytext=(0,12), ha='center', fontsize=9, fontweight='bold')
    ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("Green GDP Gap (%)", fontsize=12)
    ax.set_title(f"{name}: Green GDP Gap Trend (2008-2018)", fontsize=15, fontweight="bold")
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_gap_trend.png"), dpi=150); plt.close()
    print(f"  [3/9] Saved: {tag}_gap_trend.png")

    # ── Chart 4: Pie — average cost breakdown ──
    ar, ac, ap = c["Res_Depl"].mean()/B, c["CO2_DMG"].mean()/B, c["PED"].mean()/B
    total = ar + ac + ap
    fig, ax = plt.subplots(figsize=(8, 8))
    sizes = [ar, ac, ap]
    labels = [f"Resource Depletion\n${ar:.1f}B ({ar/total*100:.1f}%)",
              f"CO₂ Damage\n${ac:.1f}B ({ac/total*100:.1f}%)",
              f"Particulate Emissions\n${ap:.1f}B ({ap/total*100:.1f}%)"]
    ax.pie(sizes, labels=labels, colors=["#FF9800","#F44336","#9C27B0"],
           explode=(0.05,0.05,0.05), startangle=140, textprops={"fontsize":11})
    ax.set_title(f"{name}: Avg Environmental Cost Breakdown (2008-2018)", fontsize=15, fontweight="bold", pad=20)
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_pie.png"), dpi=150); plt.close()
    print(f"  [4/9] Saved: {tag}_pie.png")

    # ── Chart 5: Sustainability index bars ──
    fig, ax = plt.subplots(figsize=(12, 5))
    cols = ["#4CAF50" if s > 0.97 else "#FF9800" if s > 0.93 else "#F44336" for s in c["Sust_Idx"]]
    bars = ax.bar(c["Year"], c["Sust_Idx"], color=cols, width=0.6, edgecolor="white")
    ax.axhline(y=1.0, color="gray", ls="--", alpha=0.5, label="Perfect Score (1.0)")
    for bar, val in zip(bars, c["Sust_Idx"]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f"{val:.4f}", ha='center', fontsize=8, fontweight='bold')
    ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("Sustainability Index", fontsize=12)
    ax.set_title(f"{name}: Sustainability Index (Green GDP / GDP) (2008-2018)", fontsize=15, fontweight="bold")
    ax.set_ylim(min(c["Sust_Idx"])*0.98, 1.01); ax.legend(fontsize=11)
    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_sustainability.png"), dpi=150); plt.close()
    print(f"  [5/9] Saved: {tag}_sustainability.png")

    # ── Chart 6: Developing nations comparison ──
    compare = ["IND","CHN","BRA","ZAF","IDN","NGA","MEX","BGD","PAK","VNM"]
    if code not in compare:
        compare.append(code)
    cmp = mg[mg["Country Code"].isin(compare)].dropna(subset=["Gap_Pct"])
    if not cmp.empty:
        avg = cmp.groupby("Country Name")["Gap_Pct"].mean().sort_values()
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ["#E91E63" if n == name else "#FF9800" if v > 5 else "#4CAF50" for n, v in avg.items()]
        ax.barh(avg.index, avg.values, color=colors, edgecolor="white", height=0.6)
        for i, (n2, v) in enumerate(avg.items()):
            ax.text(v + 0.15, i, f"{v:.1f}%", va="center", fontsize=10, fontweight="bold")
        ax.set_xlabel("Avg Green GDP Gap (%)", fontsize=12)
        ax.set_title(f"Developing Nations Comparison (2008-2018) — {name} highlighted", fontsize=14, fontweight="bold")
        plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f"{tag}_comparison.png"), dpi=150); plt.close()
        print(f"  [6/9] Saved: {tag}_comparison.png")

    # ── Chart 7: Correlation Matrix Heatmap ──
    corr_vars = c[['GDP', 'Green_GDP', 'Res_Depl', 'CO2_DMG', 'PED', 'Env_Deg', 'NNCC']]
    corr_matrix = corr_vars.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".3f",
                linewidths=0.5, ax=ax, square=True)
    ax.set_title(f'{name}: Correlation Matrix of Economic & Environmental Indicators', fontsize=14, fontweight='bold')
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f'{tag}_correlation_matrix.png'), dpi=150); plt.close()
    print(f"  [7/9] Saved: {tag}_correlation_matrix.png")

    # ── Chart 8: Decoupling Elasticity Over Time ──
    ce = c.dropna(subset=['CO2_Elasticity'])
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(ce["Year"], ce["CO2_Elasticity"], color=["#F44336" if e >= 1 else "#4CAF50" for e in ce["CO2_Elasticity"]],
           width=0.6, edgecolor="white", label="CO₂/GDP Elasticity")
    ax.axhline(y=1.0, color="black", ls="--", lw=1.5, alpha=0.7, label="Coupling Threshold (1.0)")
    ax.axhline(y=0, color="gray", ls="-", lw=0.5, alpha=0.3)
    for _, r in ce.iterrows():
        ax.text(r['Year'], r['CO2_Elasticity'] + 0.05, f"{r['CO2_Elasticity']:.2f}",
                ha='center', fontsize=9, fontweight='bold')
    ax.set_xlabel("Year", fontsize=12); ax.set_ylabel("Elasticity (CO₂ growth / GDP growth)", fontsize=12)
    ax.set_title(f"{name}: CO₂ Damage Decoupling Elasticity (2009-2018)", fontsize=15, fontweight="bold")
    ax.legend(fontsize=11); ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f'{tag}_decoupling.png'), dpi=150); plt.close()
    print(f"  [8/9] Saved: {tag}_decoupling.png")

    # ── Chart 9: Polynomial Forecast to 2030 ──
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [2, 1]})

    # Top: GDP vs Green GDP forecast
    ax1.plot(X, y_gdp/B, 'o', color='#2196F3', ms=8, label='Actual GDP', zorder=5)
    ax1.plot(years_all, pred_gdp/B, '--', color='#2196F3', alpha=0.6, lw=2, label='Forecast GDP')
    ax1.plot(X, y_green/B, 's', color='#4CAF50', ms=8, label='Actual Green GDP', zorder=5)
    ax1.plot(years_all, pred_green/B, '--', color='#4CAF50', alpha=0.6, lw=2, label='Forecast Green GDP')
    ax1.fill_between(years_all, pred_green/B, pred_gdp/B, alpha=0.1, color='#F44336', label='Projected Gap')
    ax1.axvline(x=2018.5, color='gray', linestyle=':', lw=2, label='Forecast Boundary')
    ax1.set_ylabel("Billion USD", fontsize=12)
    ax1.set_title(f"{name}: GDP & Green GDP Polynomial Forecast to 2030", fontsize=15, fontweight="bold")
    ax1.legend(fontsize=10, loc='upper left'); ax1.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax1.grid(True, alpha=0.3)

    # Bottom: Projected Gap %
    proj_gap = ((pred_gdp - pred_green) / pred_gdp * 100)
    ax2.plot(years_all, proj_gap, 'D-', color='#E91E63', lw=2, ms=6)
    ax2.fill_between(years_all, proj_gap, alpha=0.15, color='#E91E63')
    ax2.axvline(x=2018.5, color='gray', linestyle=':', lw=2)
    ax2.set_xlabel("Year", fontsize=12); ax2.set_ylabel("Projected Gap (%)", fontsize=12)
    ax2.set_title(f"Projected Green GDP Gap (%) Through 2030", fontsize=13, fontweight="bold")
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax2.grid(True, alpha=0.3)

    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, f'{tag}_forecast_2030.png'), dpi=150); plt.close()
    print(f"  [9/9] Saved: {tag}_forecast_2030.png")

    # ═══════════════════════════════════════════════════════════
    # SECTION 6: EXPORT DATA TO CSV
    # ═══════════════════════════════════════════════════════════
    export_cols = ['Year', 'GDP', 'GNI', 'NRD_PCT', 'CO2_DMG', 'PED',
                   'Res_Depl', 'Env_Deg', 'NNCC', 'Green_GDP', 'Gap_Pct', 'Sust_Idx']
    c[export_cols].to_csv(os.path.join(OUTPUT_DIR, f"{tag}_green_gdp_data.csv"), index=False)
    print(f"\n  Exported: {tag}_green_gdp_data.csv")

    # Export forecast
    forecast_df = pd.DataFrame({
        'Year': years_all,
        'Projected_GDP': pred_gdp,
        'Projected_Green_GDP': pred_green,
        'Projected_NNCC': pred_nncc,
        'Projected_Gap_Pct': proj_gap
    })
    forecast_df.to_csv(os.path.join(OUTPUT_DIR, f"{tag}_forecast_2030.csv"), index=False)
    print(f"  Exported: {tag}_forecast_2030.csv")

    print(f"\n{'='*100}")
    print(f"  ALL OUTPUTS SAVED TO: {OUTPUT_DIR}")
    print(f"{'='*100}")

if __name__ == "__main__":
    main()
        