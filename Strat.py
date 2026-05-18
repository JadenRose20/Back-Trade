import pandas as pd
import vectorbt as vbt
import matplotlib.pyplot as plt

df = pd.read_csv("MNQ_Data.csv")

df["DateTime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"]
)

print(df.head())