import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings

warnings.filterwarnings("ignore")

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

def main():
    code = COUNTRY_CODE.upper()
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

    mg["Res_Depl"] = (mg["NRD_PCT"] / 100) * mg["GNI"]
    mg["Env_Deg"] = mg["CO2_DMG"] + mg["PED"]
    mg["NNCC"] = mg["Res_Depl"] + mg["Env_Deg"]
    mg["Green_GDP"] = mg["GDP"] - mg["NNCC"]

    c = mg[mg["Country Code"] == code].dropna().sort_values("Year").reset_index(drop=True)
    
    print("--- ADVANCED ANALYTICS FOR BANGLADESH ---")
    
    # 1. Decoupling Analysis (Elasticity of Emissions to GDP)
    # E = (% change in Env Deg) / (% change in GDP)
    c['GDP_Growth'] = c['GDP'].pct_change()
    c['EnvDeg_Growth'] = c['Env_Deg'].pct_change()
    c['CO2_Growth'] = c['CO2_DMG'].pct_change()
    
    # Calculate elasticity
    c['Decoupling_Elasticity'] = c['CO2_Growth'] / c['GDP_Growth']
    
    avg_elasticity = c['Decoupling_Elasticity'].mean()
    print(f"\nAverage CO2/GDP Elasticity (2009-2018): {avg_elasticity:.2f}")
    if avg_elasticity < 1 and avg_elasticity > 0:
        print("Finding: Relative Decoupling is occurring. Emissions are growing slower than GDP.")
    elif avg_elasticity < 0:
        print("Finding: Absolute Decoupling is occurring. Emissions are falling while GDP grows.")
    else:
        print("Finding: No Decoupling. Emissions are growing faster than or equal to GDP.")

    # 2. Correlation Matrix
    corr_vars = c[['GDP', 'Green_GDP', 'Res_Depl', 'CO2_DMG', 'PED', 'Env_Deg']]
    corr_matrix = corr_vars.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f")
    plt.title('Correlation Matrix of Economic & Environmental Indicators (Bangladesh)', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'bangladesh_correlation_matrix.png'), dpi=150)
    plt.close()
    print("Saved correlation matrix plot.")

    # 3. Future Forecasting (Polynomial Regression Degree 2)
    # We will forecast next 5 years (2019-2023)
    X = c['Year'].values
    y_gdp = c['GDP'].values
    y_green = c['Green_GDP'].values
    y_env = c['Env_Deg'].values
    
    # Fit degree 2 polynomial
    p_gdp = np.polyfit(X, y_gdp, 2)
    p_green = np.polyfit(X, y_green, 2)
    p_env = np.polyfit(X, y_env, 2)
    
    years_future = np.array(range(2008, 2024))
    pred_gdp = np.polyval(p_gdp, years_future)
    pred_green = np.polyval(p_green, years_future)
    pred_env = np.polyval(p_env, years_future)
    
    plt.figure(figsize=(12, 6))
    plt.plot(X, y_gdp / 1e9, 'o', color='blue', label='Actual GDP')
    plt.plot(years_future, pred_gdp / 1e9, '--', color='blue', alpha=0.5, label='Forecast GDP')
    
    plt.plot(X, y_green / 1e9, 's', color='green', label='Actual Green GDP')
    plt.plot(years_future, pred_green / 1e9, '--', color='green', alpha=0.5, label='Forecast Green GDP')
    
    plt.axvline(x=2018, color='gray', linestyle=':', label='Forecast Start')
    plt.title('Polynomial Forecast: GDP vs Green GDP (Bangladesh 2008-2023)', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Billion USD')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'bangladesh_forecast.png'), dpi=150)
    plt.close()
    print("Saved forecast plot.")

    print("\nForecasted Values for 2023:")
    print(f"Projected GDP (2023): ${pred_gdp[-1]/1e9:.2f} B")
    print(f"Projected Green GDP (2023): ${pred_green[-1]/1e9:.2f} B")
    print(f"Projected Gap % (2023): {((pred_gdp[-1] - pred_green[-1]) / pred_gdp[-1] * 100):.2f}%")

if __name__ == "__main__":
    main()
      