# H: Parking duration are longer during vacation times
from google.colab import auth
import pandas as pd

# Authenticate in BQ
auth.authenticate_user()

# Import the BQ table into Python
query = '''SELECT *
FROM `parking-transactions.main.parking_transactions_cleaned_final`
WHERE RAND() < 500000.0 / 15044715.0
LIMIT 500000'''

df = pd.read_gbq(query, project_id="parking-transactions")
df

# We first need to define holidays periods. According to research (https://www.redcort.com/us-federal-bank-holidays, https://aytm.com/post/vacations-survey),
# most americans take their holidays in June and July. The vacation period will be set between June 1st and July 31st to account for the most tourists.
# We will also include Memorial Day, Independence Day, Labor Day, Thanksgiving, with a buffer as most companies offer paid time off during these days

# Define vacation periods for each year
vacation_periods = []
years = range(2019, 2025)

for year in years:
    # Winter holidays
    winter_start = pd.to_datetime(f'{year}-12-20')
    winter_end = pd.to_datetime(f'{year + 1}-01-05')
    vacation_periods.append((winter_start, winter_end))

    # Summer break
    summer_start = pd.to_datetime(f'{year}-06-01')
    summer_end = pd.to_datetime(f'{year}-07-31')
    vacation_periods.append((summer_start, summer_end))

    # Memorial Day:
    memorial_day_start = pd.to_datetime(f'{year}-05-25')
    memorial_day_end = pd.to_datetime(f'{year}-05-26')
    vacation_periods.append((memorial_day_start, memorial_day_end))

    # Independence Day:
    independence_day_start = pd.to_datetime(f'{year}-07-03')
    independence_day_end = pd.to_datetime(f'{year}-07-04')
    vacation_periods.append((independence_day_start, independence_day_end))

    # Labor Day:
    labor_day_start = pd.to_datetime(f'{year}-08-31')
    labor_day_end = pd.to_datetime(f'{year}-09-01')
    vacation_periods.append((labor_day_start, labor_day_end))

    # Thanksgiving:
    thanksgiving_start = pd.to_datetime(f'{year}-11-26')
    thanksgiving_end = pd.to_datetime(f'{year}-11-27')
    vacation_periods.append((thanksgiving_start, thanksgiving_end))

# Create a column indicating whether the parking time is during vacation
df['is_vacation'] = False
for start, end in vacation_periods:
    df['is_vacation'] = df['is_vacation'] | ((df['start_time'] >= start) & (df['start_time'] <= end))

# Group by vacation status and calculate mean duration
duration_stats = df.groupby('is_vacation')['duration_minutes'].mean()
print(duration_stats)

# Perform a t-test

# With H0: There is no difference in parking duration between non-vacation time and vacation time
vacation_durations = df[df['is_vacation']]['duration_minutes']
non_vacation_durations = df[~df['is_vacation']]['duration_minutes']

t_stat, p_value = ttest_ind(vacation_durations, non_vacation_durations, equal_var=False)
print(f'T-statistic: {t_stat}, P-value: {p_value}')
# Since p<0.5, H0 can be rejected.

# However, the variation in the mean is not that significant.

import matplotlib.pyplot as plt
import seaborn as sns

# Plot the distribution of parking durations
plt.figure(figsize=(10, 6))
sns.boxplot(x='is_vacation', y='duration_minutes', data=df)
plt.title('Distribution of Parking Durations by Vacation Status')
plt.xlabel('Is Vacation')
plt.ylabel('Duration (minutes)')
plt.show()
