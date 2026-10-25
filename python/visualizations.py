import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

df = pd.read_csv("cookie_cats.csv")

gate_30 = df[df['version'] == 'gate_30']['sum_gamerounds']
gate_40 = df[df['version'] == 'gate_40']['sum_gamerounds']

#Histograms of the Distribution of Gamerounds
plt.hist(gate_30, bins=50, range=(0, 200), edgecolor='black', density=True, label='Gate 30')
plt.hist(gate_40, bins=50, range = (0, 200), edgecolor='black', density=True, label='Gate 40')
plt.title('Distribution of Gamerounds for Gate 30')
plt.xlabel('Number of Gamerounds')
plt.ylabel('Frequency')
plt.legend()
plt.show()

#Bar Chart of Gate 30 and Gate 40 Day 1 and Day 7 retention percentages

labels = ("Gate 30", "Gate 40")
retention = {
    'Day 1': (0.45, 0.44),
    'Day 7': (0.1902, 0.182)
}

fig, ax = plt.subplots(layout='constrained')
x = np.arange(len(labels))
width = 0.35

bars1 = ax.bar(x - width/2, retention['Day 1'], width, label='Day 1')
bars2 = ax.bar(x + width/2, retention['Day 7'], width, label='Day 7')

ax.set_ylabel('Percent')
ax.set_title('Percent of players retained')
ax.legend(loc='upper left', ncol=2)
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.set_ylim(0,0.55)
ax.set_xticks(x, labels)

for bars in (bars1, bars2):
    ax.bar_label(
        bars,
        labels=[f"{value:.1%}" for value in bars.datavalues],
        padding=3
    )
plt.show()
