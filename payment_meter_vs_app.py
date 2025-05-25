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

df.info()
df.shape

H1: Payment meters are less used over time than App payment
# Verifying there is no null values
df[df['payment_method']==0].shape

# Checking unique values
df['payment_method'].unique()

df['payment_method'].value_counts()

# Grouping the payement methods into 3 groups: App, Meter and Other

payment_mapping = {
    # App payments
    'App - Wallet': 'App - Paid',
    'Apple Pay': 'App - Paid',
    'App - Credit Card': 'App - Paid',
    'Google Pay': 'App - Paid',

    # Meter payment
    'CARD' : 'Meter',
    'COINS' : 'Meter',

    # Other payment
    'App - Free' : 'App - Other',
    'App - Validation': 'App - Other'

}
# adding a column with the newly mapped payment method
df['payment_method_mapped'] = df['payment_method'].map(payment_mapping)

# Converting the start_time and end_time to date_time
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Extracting the month from the start_time
df['month'] = df['start_time'].dt.to_period('M')

# Group by month and payment method, then count occurrences
df_grouped = df.groupby(['month', 'payment_method_mapped']).size().reset_index(name='counts')
df_grouped.head()

# Converting the month column to a string to be able to plot it
df_grouped['month'] = df_grouped['month'].astype(str)

# Plotting the data
import plotly.express as px

fig = px.line(df_grouped, x='month', y='counts', color='payment_method_mapped',
              title='Evolution of Payment Methods Over Time',
              labels={'counts': 'Number of Transactions', 'quarter': 'Quarter'})

fig.update_layout(xaxis_title='Quarter', yaxis_title='Number of Transactions')
fig.show()

# It seems that Meter payment steadily declined since October 2022, and were then surpassed in October 2023 by App paiment