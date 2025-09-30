import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv('Carbase.csv')
df.index = [df["Name"][0],df["Name"][1],df["Name"][2]]
df['Sales'].plot(kind = 'barh', color="violet")
plt.xlabel('Дні тижня')
plt.title('Середньодобова температура за тиждень')
plt.show()