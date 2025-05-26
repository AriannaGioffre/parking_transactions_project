# Hypothesis: People paying via app spend more than people paying via parking meters
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
df.head()

# Average of the amount paid for each payment method
df.groupby(['payment_method_mapped']).mean('amount')

# Median of the amount paid for each payment method
df.groupby('payment_method_mapped')['amount'].median()

import plotly.express as px
px.box(df, x='payment_method_mapped', y='amount', title='Amount Paid by Payment Method')

from scipy.stats import ttest_ind

# With HO: There is no difference in the average amount spent between people paying via the app and those paying via parking meters.
# And H1: There is a difference in the average amount spent between the two groups.

# Separate the amount data for each payment method
app_paid_amounts = df[df['payment_method_mapped'] == 'App - Paid']['amount']
meter_amounts = df[df['payment_method_mapped'] == 'Meter']['amount']

# Perform a t-test
t_stat, p_value = ttest_ind(app_paid_amounts, meter_amounts, equal_var=False)
print(f'T-statistic: {t_stat}, P-value: {p_value}')

# HO can be rejected. There are very small differences between the mean and median.
