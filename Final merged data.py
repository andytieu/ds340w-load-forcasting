import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))

energy = pd.read_csv(os.path.join(base_path, "merged_df.csv"))
weather = pd.read_csv(os.path.join(base_path, "hourly_weather_newark.csv"))
res = pd.read_excel(os.path.join(base_path, "Res_cleaned.xlsx"))

energy["Month"] = pd.to_datetime(energy["Month"], format="%b %Y", errors="coerce")

weather["Time"] = pd.to_datetime(weather["Time"], errors="coerce").dt.round("H")
weather_hourly = weather.groupby("Time").mean(numeric_only=True).reset_index().rename(columns={"Time":"Hour"})

res["Date"] = pd.to_datetime(res["Date"], errors="coerce").dt.round("H")
res_hourly = res.dropna(subset=["Date"]).rename(columns={"Date":"Hour"})

hourly = pd.merge(res_hourly, weather_hourly, on="Hour", how="inner")

hourly["Month"] = hourly["Hour"].dt.to_period("M").dt.to_timestamp()
final = pd.merge(hourly, energy, on="Month", how="inner").drop(columns=["Month"])

final.to_csv(os.path.join(base_path, "final_merged_dataset_hourly.csv"), index=False)
print("Rows x Cols:", final.shape)
print(final.head())
