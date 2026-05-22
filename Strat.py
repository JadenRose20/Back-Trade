import pandas as pd
import vectorbt as vbt
import matplotlib.pyplot as plt

df = pd.read_csv("MNQ_Data.csv")

df["DateTime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"]
)
df = df.set_index("DateTime")

price = df["Close"]

fastMA = vbt.MA.run(price, window=2)
slowMA = vbt.MA.run(price, window=50)

entry = fastMA.ma_crossed_above(slowMA)
exit = fastMA.ma_crossed_below(slowMA)

pf = vbt.Portfolio.from_signals(
    close=price,
    entries=entry,
    exits=exit,
    init_cash=100000,
    size=1,
    size_type=("amount"),
    fees=0,
    slippage=0.0001,
    freq="1min"
)

# Futures modifiers
contracts = 1
point_multi = 2.00
round_trip_commission = 3.00

trades = pf.trades.records_readable.copy()

# print(trades.to_string())
trades["Points"] = trades["Avg Exit Price"] - trades["Avg Entry Price"]
trades["Futures PnL"] = trades["Points"] * point_multi * contracts
trades["Net Futures PnL"] = trades["Futures PnL"] - round_trip_commission

# print(trades[[
#     "Exit Timestamp",
#     "Avg Entry Price",
#     "Avg Exit Price",
#     "Points",
#     "Futures PnL",
#     "Net Futures PnL"
# ]])

print(trades)
print(trades["Net Futures PnL"].sum())
# trades.to_csv("Trades")
# # Plot moving averages
# df["fastMA"] = fastMA.ma
# df["slowMA"] = slowMA.ma

# df[["Close", "fastMA", "slowMA"]].plot(figsize=(15, 7))

# one_week_df = df["DateTime"]

# plt.show()

# # Interactive portfolio chart
# pf.plot().show()
# ##>