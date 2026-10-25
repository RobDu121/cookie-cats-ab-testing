from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
from scipy.stats import trim_mean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("cookie_cats.csv")
gate_30 = df[df['version'] == 'gate_30']['sum_gamerounds']
gate_30_filtered = df[(df['version'] == 'gate_30') & df['userid'] != 6390605]['sum_gamerounds']
gate_40 = df[df['version'] == 'gate_40']['sum_gamerounds']

# Sample sizes
n_30 = 44700
n_40 = 45489

# Players retained after 7 days
r_30 = 8502
r_40 = 8279

# Sample proportions
p_30 = r_30 / n_30
p_40 = r_40 / n_40

# Difference in proportions
difference = p_30 - p_40

# Number of players retained after 7 days
retained = [8502, 8279]

# Total number of players in each group
total_players = [44700, 45489]

# Significance level
alpha = 0.05

# Perform two-proportion z-test
z_stat, p_value = proportions_ztest(
    count=retained,
    nobs=total_players,
    alternative='two-sided'
)
print("Z-test")
print("Z-statistic:", z_stat)
print("P-value:", p_value)

if p_value < alpha:
    print("There is a significant difference in retention rates between the two groups.")
else:
    print("There is no significant difference in retention rates between the two groups.")

standard_error = np.sqrt(p_30 * (1 - p_30) / n_30 + p_40 * (1 - p_40) / n_40)
upper_bound = difference + 1.96 * standard_error
lower_bound = difference - 1.96 * standard_error

print("95% Confidence Interval for the difference in proportions: [", lower_bound, ", ", upper_bound, "]")

#Welch's t-test
t_stat, p_value2 = ttest_ind(
    gate_30, gate_40, equal_var = False
)
print("Welch's t-test:")
print("T-statistic:", t_stat)
print("P-value:", p_value2)

#Welch's t-test without outlier
t_stat2, p_value3 = ttest_ind(
    gate_30_filtered, gate_40, equal_var=False
)
print("Welch's t-test without outlier:")
print("T-statistic:", t_stat2)
print("P-value:", p_value3)

#Yuen's trimmed t-test
t_stat3, p_value4 = ttest_ind(
    gate_30, gate_40, equal_var=False, trim=0.05
)
print("Yuen's trimmed t-test:")
print("T-statistic:", t_stat3)
print("P-value:", p_value4)

