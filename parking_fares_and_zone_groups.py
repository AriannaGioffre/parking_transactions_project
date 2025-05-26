#H0: Parking fares vary based on the app_zone_group

from google.colab import auth
import pandas as pd

# Will collect your credentials
auth.authenticate_user()

# Query Bigquery
query = "SELECT  app_zone_group, amount, duration_minutes, SAFE_DIVIDE(amount,duration_minutes) AS fare_per_min, payment_method FROM `parking-transactions.main.parking_transactions_cleaned_final` WHERE RAND() < 700000.0 / 15044715.0 LIMIT 700000"
project = "parking-transactions"

df_draft = pd.read_gbq(query, project_id=project)

#removed all the rows where duration minutes are null
df = df_draft[df_draft['duration_minutes'] != 0] 

#average fare per app_zone_group sorted by descending order
df.groupby('app_zone_group')['fare_per_min'].mean().sort_values(ascending=False)

#most of the app_zone_groups have average fare around 0,04, however there are some exceptions like 'Silicon and Titanium' with 1.36

#plotting box plots figure
import plotly.express as px
fig = px.box(df, x='app_zone_group', y='fare_per_min')
fig.show()

#Grouping the app_zone_group into three main categories
app_zone_group_fares = {
    # Core
    'Silicon and Titanium': 'Core',
    'CORE': 'Core',
    'SoCo PTMD': 'Core',
    'East Austin PTMD': 'Core',
    'West Campus PBD': 'Core',
    'Mueller PTMD': 'Core',
    'Colorado River Area PTMD': 'Core',
    'Austin High': 'Core',
    'Woods of Westlake': 'Core',

    # Non-Core
    'Non-Core': 'Non-Core',
    'Non-Core (Rainey)': 'Non-Core',
    'Non-Core (Lee Barton)': 'Non-Core',
    'Non-Core (Walsh)': 'Non-Core',
    'Non-Core (Toomey)': 'Non-Core',

    # Other
    'Austin FC': 'Other',
    'IH-35 Lot': 'Other',
    'MOPAC Lot': 'Other',
    'MACC Lot': 'Other',
    'PARD (Walsh Boat Lot)': 'Other',
    'PARD (Butler Lot)': 'Other',
    'PARD (Parking Lots)': 'Other',
    'PARD (Walsh Upper Lot)': 'Other',
    'No Zone Group': 'Other'
}

df['app_zone_group_fares'] = df['app_zone_group'].map(app_zone_group_fares)

#performing the Anova tests to check if there is any statistical difference in terms of fares among the three categories

df_CORE = df[df['app_zone_group_fares'] == 'Core']
df_Non_CORE = df[df['app_zone_group_fares']== 'Non-Core']
df_other = df[df['app_zone_group_fares'] =='Other']

import scipy.stats as stats

a_score, p_value = stats.f_oneway(df_CORE['fare_per_min'].dropna(), df_Non_CORE['fare_per_min'].dropna(), df_other['fare_per_min'].dropna())

print(f'p-value: {p_value}')

#p-value = 0.0017967414482253415 < 0.05 indicating that there is a difference in the mean fare among the different app_zone_groups
