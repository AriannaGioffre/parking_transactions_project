# Checking for primary key in the ID column. 

SELECT
  ID,
  COUNT(*) AS nb
FROM `parking-transactions.main.parking_transactions`
GROUP BY ID
HAVING nb >1; -- No data to display, ID is the primary key 

# Checking for nulls in the ID columns: O
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE ID IS NULL;

# Checking for nulls in source: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE Source IS NULL;

# Checking for nulls in duration_minutes: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE DurationinMinutes IS NULL;

# Checking for nulls in StartTime: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE StartTime IS NULL;

# Checking for nulls in EndTime: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE EndTime IS NULL;

# Checking for nulls in Amount: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE Amount IS NULL;

# Checking for nulls in PaymentMethod: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE PaymentMethod IS NULL;

# Checking for nulls in LocationGroup: 19
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE LocationGroup IS NULL;

# Checking which LocationGroup are nulls
SELECT
  *
FROM `parking-transactions.main.parking_transactions`
WHERE LocationGroup IS NULL;

SELECT
  *
FROM `parking-transactions.main.parking_transactions`
WHERE AppZoneID = 101.0; -- All nulls LocationGroup seems tied to the AppZoneID 101.0, which could be a false location

SELECT
  DISTINCT(AppZoneID)
FROM `parking-transactions.main.parking_transactions`
ORDER BY AppZoneID; -- Seems to be a false location, as all the others having a 6 letter code. 

-- THESE SEEMS TO BE OUTLIERS, I Would remove the nulls, 101.0 and the ones with 8 digits.

# Counting distinct in LocationGroup: 27 
SELECT
  DISTINCT(LocationGroup)
FROM `parking-transactions.main.parking_transactions`
ORDER BY LocationGroup;

# Checking for nulls in AppZoneID: 8240734
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE AppZoneID IS NULL;

# Checking for nulls in AppZoneGroup: 8240734
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE AppZoneGroup IS NULL;

# Check where the AppZoneID and AppZoneGroup are nulls 
SELECT
  Source,
  COUNT(*) AS nb_of_rows
FROM `parking-transactions.main.parking_transactions`
WHERE AppZoneGroup IS NULL AND AppZoneID IS NULL
GROUP BY Source;

/* All nulls are related to parking meters, it could mean two things: 
1) The App columns refers to when the customer is paying with the app
2) The app does not cover the area. */

SELECT
  DISTINCT(Source)
FROM `parking-transactions.main.parking_transactions`;

-- Checking to see if 1) is true -> No data to display, seems true
SELECT
  Source, 
  Amount, 
  AppZoneGroup, 
  AppZoneID
FROM `parking-transactions.main.parking_transactions`
WHERE Source = 'Passport - app' AND AppZoneGroup IS NULL;

-- Checking for nulls in LastUpdated: 0
SELECT
  COUNT(*) as null_count
FROM `parking-transactions.main.parking_transactions`
WHERE LastUpdated IS NULL;