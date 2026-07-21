import pandas as pd
import numpy as np
details={
    "Name": ["varsha","anusha","shenba","santhya","ramakani"],
    "Dept":["it","cs","it","cs","it"],
    "salary":[1000,2000,6000,8000,7000]
}
df = pd.DataFrame(details)
print(df)
print(df.info())
print(df.head())
print(df.shape)
print(df.describe())
print(df.columns)
print(df["salary"])
print(df[["Name", "salary"]])
print(df.loc[0])
print(df.loc[3])
print(df.loc[0:4])
high=df[(df["salary"]>2000)]
h_dept=df[(df["Dept"]=="it")]
print(high)
print(h_dept)
df["bonus"] = df["salary"] * 0.10
print(df)