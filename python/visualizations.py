import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "cookie_cats.csv"

df = pd.read_csv(data_path)

gate_30 = df[df['version'] == 'gate_30']['sum_gamerounds']
gate_40 = df[df['version'] == 'gate_40']['sum_gamerounds']

#Histograms of the Distribution of Gamerounds
plt.hist(gate_30, bins=50, range=(0, 200), edgecolor='black', density=True, label='Gate 30')
plt.hist(gate_40, bins=50, range = (0, 200), edgecolor='black', density=True, label='Gate 40')
plt.title('Distribution of Gamerounds for Gate 30')
plt.xlabel('Number of Gamerounds')
plt.ylabel('Frequency')
plt.legend()
plt.savefig("distribution_gamerounds.png",
            dpi=300, bbox_inches="tight")
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
plt.savefig("figures/retention_comparison.png",
        dpi=300, bbox_inches="tight")
plt.show()

#95% Confidence Interval Graph
n_30 = 44700
n_40 = 45489

r_30 = 8502
r_40 = 8279

p_30 = r_30 / n_30
p_40 = r_40 / n_40

difference = p_30 - p_40
standard_error = np.sqrt(p_30 * (1 - p_30) / n_30 + p_40 * (1 - p_40) / n_40)
upper_bound = difference + 1.96 * standard_error
lower_bound = difference - 1.96 * standard_error
effect = difference * 100
lower = lower_bound * 100
upper = upper_bound * 100

left_error = effect - lower
right_error = upper - effect

fig, ax = plt.subplots()
ax.errorbar(effect, 0, xerr=[[left_error], [right_error]], fmt='o', capsize=5)
ax.axvline(x=0, linestyle="--")

ax.set_xlabel("Difference in Day 7 Retention (pp)")
ax.set_yticks([])
ax.set_title("Gate 30 vs Gate 40: Treatment Effect")

ax.text(effect, 0.02, f"{effect:.2f} pp", ha='center')
plt.savefig("figures/confidence_interval.png",
            dpi=300, bbox_inches="tight")
plt.show()
