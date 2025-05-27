#HO: parking durations during weekend are generally longer than during weekdays

# Query Bigquery
query_dates = "SELECT  start_time, end_time, app_zone_group, amount, duration_minutes, SAFE_DIVIDE(amount,duration_minutes) AS fare_per_min, payment_method FROM `parking-transactions.main.parking_transactions_cleaned_final` WHERE RAND() < 500000.0 / 15044715.0 AND duration_minutes != 0 LIMIT 500000"
project = "parking-transactions"

df_dates = pd.read_gbq(query_dates, project_id=project)

#convert start__time and end_time into datetime format
df_dates['start_time'] = pd.to_datetime(df_dates['start_time'])
df_dates['end_time'] = pd.to_datetime(df_dates['end_time'])
df_dates.head()

#function to verify if the parking period includes Saturday and/or Sunday
def has_weekend(start, end):
    date_range = pd.date_range(start.date(), end.date(), freq='D')
    return any(date.weekday() >= 5 for date in date_range)  # 5=Saturday, 6=Sunday

# Apply the function
df_dates['contains_weekend'] = df_dates.apply(lambda row: has_weekend(row['start_time'], row['end_time']), axis=1)

# Display the result
print(df_dates[['start_time', 'end_time', 'contains_weekend']])

#add column to provide the day number
df_dates['start_time_day'] = df_dates['start_time'].dt.weekday + 1
df_dates['end_time_day'] = df_dates['end_time'].dt.weekday + 1
#Sunday is 7 and Monday is 1

#calculate the average duration if it contains weekend and if it does not
avg_durations = df_dates.groupby('contains_weekend')['duration_minutes'].mean()
print(avg_durations)

##result:
#contains_weekend
#False    124.771029
#True     152.470692
#So if it contains the weekend, on average the duration is higher

#plot the graph
import matplotlib.pyplot as plt

avg_durations.plot(kind='bar', title='Average Parking Duration: Weekend vs Weekday')
plt.xticks([0,1], ['False', 'True'], rotation=0)
plt.ylabel('Average Duration (minutes)')
plt.show()

#calculate the difference in days between end_time and start_time
diff_days = df_dates['end_time'] - df_dates['start_time']
df_dates['diff_days'] = diff_days.dt.days

#create a new column which will split the parking transacations into 3 main categories: one day, more days- weekend, more days -weekday 
def categorize_duration(row):
    if row['diff_days'] == 0:
        return 'one day'
    else:
        if row['contains_weekend'] == True:
            return 'more days - weekend'
        else:
            return 'more days - week'

df_dates['duration_category'] = df_dates.apply(categorize_duration, axis=1)

#by filtering by 'more days - week' we get only one row/parking transaction. This means that in most of the cases, if the parking transaction last more than one  day, then it includes the weekend
df_dates[df_dates['duration_category'] == 'more days - week']

#this can also be observed by plotting the box plot
px.box(df_dates, x='duration_category', y='duration_minutes')