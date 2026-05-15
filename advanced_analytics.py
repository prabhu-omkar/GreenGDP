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
    

if __name__ == '__main__':
    main()
