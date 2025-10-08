import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))

energy_df = pd.read_csv(os.path.join(base_path, "merged_df.csv"))
energy_df["Month"] = pd.to_datetime(energy_df["Month"], errors="coerce")
energy_df.to_csv(os.path.join(base_path, "energy_cleaned.csv"), index=False)
print("Energy data cleaned:", energy_df.shape)

weather_df = pd.read_csv(os.path.join(base_path, "hourly_weather_newark.csv"))
weather_df["Time"] = pd.to_datetime(weather_df["Time"], errors="coerce")
weather_df["Month"] = weather_df["Time"].dt.to_period("M").dt.to_timestamp()
weather_monthly = weather_df.groupby("Month").mean(numeric_only=True).reset_index()
weather_monthly.to_csv(os.path.join(base_path, "weather_cleaned_monthly.csv"), index=False)
print("Weather monthly cleaned:", weather_monthly.shape)

res_df = pd.read_excel(os.path.join(base_path, "Res_cleaned.xlsx"))
res_df["Date"] = pd.to_datetime(res_df["Date"], errors="coerce")
res_df["Month"] = res_df["Date"].dt.to_period("M").dt.to_timestamp()
res_monthly = res_df.groupby("Month")["Res"].mean().reset_index()
res_monthly.to_csv(os.path.join(base_path, "res_cleaned_monthly.csv"), index=False)
print("RES monthly cleaned:", res_monthly.shape)

merged1 = pd.merge(energy_df, weather_monthly, on="Month", how="inner")
final_merged = pd.merge(merged1, res_monthly, on="Month", how="inner")
final_merged.to_csv(os.path.join(base_path, "final_merged_dataset.csv"), index=False)

print("Final merged dataset:", final_merged.shape)
print(final_merged.head())

