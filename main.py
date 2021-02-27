import pandas as pd

daily_df = pd.read_csv("data/daily_report.csv")
total_df = (
    daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
)
total_df = total_df.rename(columns={"index": "condition"})
