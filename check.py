import pandas as pd
df=pd.read_csv("output6.csv")
fig=px.scatter(df["Avg_GPU_Usage"].values,df["Time"].values)
plt.plot(df["Avg_GPU_Usage"].values,df["Time"].values)