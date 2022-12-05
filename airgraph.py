import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("co2.csv")
print(data.head())

plt.scatter(data.iloc[:, 0], data.iloc[:, 2])
plt.show()
