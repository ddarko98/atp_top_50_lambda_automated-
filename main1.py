
'''
.Kreiraj AWS Lambda funkciju koja:

čita podatke iz ATP Tennis 2000–2025 (Daily Update) dataseta (sa Kaggle platforme – način po izboru);
analizira podatke i za svako pokretanje pravi CSV izveštaj sa top 50 igrača i sledećim kolonama:
player_name (ime i prezime),
total_wins (ukupan broj pobeda),
grand_slem_wins (pobede na Grand Slam turnirima),
atp1000_wins (pobede na ATP 1000 turnirima),
atp500_wins (pobede na ATP 500 turnirima),
first_win (datum prve pobede),
last_win (datum poslednje pobede).

'''


import kagglehub
import pandas as pd
from datetime import datetime

path = kagglehub.dataset_download("dissfya/atp-tennis-2000-2023daily-pull")
print("Path to dataset files:", path)

df = pd.read_csv(f"{path}/atp_tennis.csv", on_bad_lines="skip")

df["Winner_Name"] = df.apply(
    lambda row: row["Player_1"] if row["Winner"] == 1 else row["Player_2"], axis=1
)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

def get_series_type(row):
    series = str(row.get("Series", "")).lower()
    tournament = str(row.get("Tournament", "")).lower()

    if "grand" in series or any(gs in tournament for gs in [
        "australian open", "roland garros", "french open", "wimbledon", "us open"
    ]):
        return "Grand Slam"
    elif "masters" in series or "1000" in series or "super 9" in series:
        return "ATP 1000"
    elif "500" in series or "international gold" in series:
        return "ATP 500"
    else:
        return "Other"

df["SeriesType"] = df.apply(get_series_type, axis=1)

players_stats = (
    df.groupby("Winner_Name")
    .agg(
        total_wins=("Winner_Name", "size"),
        grand_slem_wins=("SeriesType", lambda x: (x == "Grand Slam").sum()),
        atp1000_wins=("SeriesType", lambda x: (x == "ATP 1000").sum()),
        atp500_wins=("SeriesType", lambda x: (x == "ATP 500").sum()),
        first_win=("Date", "min"),
        last_win=("Date", "max"),
    )
    .reset_index()
    .rename(columns={"Winner_Name": "player_name"})
)

report_df = players_stats.sort_values(by="total_wins", ascending=False).head(50)

report_df["first_win"] = report_df["first_win"].dt.strftime("%Y-%m-%d")
report_df["last_win"] = report_df["last_win"].dt.strftime("%Y-%m-%d")

output_file = f"top50_players_report_{datetime.today().date()}.csv"
report_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Izveštaj kreiran: {output_file}")
print(report_df.head(10))