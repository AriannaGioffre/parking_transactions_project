# Load the dataset downloaded from Kaggle with Pandas 
import pandas as pd
df = pd.read_csv("/kaggle/input/parking-transactions/Parking_Transactions.csv", low_memory=False)

#BigQuery returns to errors once we try to upload into a table with an authoschema: datetime format isn't correct, and column's names are problematic

# 1. Rename columns
df.columns = [col.strip().replace(" ", "").replace("-", "").replace("/", "") for col in df.columns]

# 2. Transform data colums keeping not deleting anything 
df['StartTime'] = pd.to_datetime(df['StartTime'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['EndTime'] = pd.to_datetime(df['EndTime'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
df['LastUpdated'] = pd.to_datetime(df['LastUpdated'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
print(df.shape)


# Export the cleaned dataset to a CSV file
df.to_csv("/content/parking_dateclean_kaggle.csv")