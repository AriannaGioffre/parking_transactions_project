# How many different payment methods we have: 10 different ones. Need to capitalize them.

SELECT 
  DISTINCT(PaymentMethod),
  COUNT(*) AS nb
FROM `parking-transactions.main.parking_transactions`
GROUP BY PaymentMethod
ORDER BY PaymentMethod;

# How many different sources we have: 3, Parking Meters, App and Web
SELECT 
  DISTINCT(Source),
  COUNT(*) AS nb
FROM `parking-transactions.main.parking_transactions`
GROUP BY Source
ORDER BY Source;

# What is the max, min amount of money spend: 147 dollars and 0 dollars.
SELECT 
  MAX(Amount) AS max_amount,
  MIN(Amount) AS min_amount
FROM `parking-transactions.main.parking_transactions`;

# What is the max and min time spend: 7201106.5 (would mean around 13 years) and -861.1, probably outliers.
SELECT 
  MAX(DurationinMinutes) AS max_duration,
  MIN(DurationinMinutes) AS min_duration
FROM `parking-transactions.main.parking_transactions`;

# Checking how many lines are negatives in DurationInMinutes: 31, need to investigate
SELECT
  ID,
  StartTime,
  EndTime,
  DurationinMinutes
FROM `parking-transactions.main.parking_transactions`
WHERE DurationinMinutes <0;

/* After further investigation, the problem was coming from end date and start date being inverted. It needs to be cleaned.*/

-- Parking in Texas is not allowed to be higher than 10 hours per session, or 600 minutes. How many are above than that ? 

SELECT 
  duration_minute,
  start_time,
  end_time,
  amount
FROM `parking-transactions.main.parking_transactions_cleaned`
WHERE duration_minute > 600; -- 150446, less than 1% of the dataset has duration longer than 10 hours.

-- There are some big outliers, probably caused because the end time was set to 2034. 
SELECT
  kiosk_id,
  duration_minute, 
  start_time,
  end_time,
  amount,
  app_zone_group,
  source
FROM `parking-transactions.main.parking_transactions_cleaned`
WHERE end_time > '2034-01-01'
ORDER BY end_time, kiosk_id DESC;

/* After further investigation, it seems impossible to book or stay longer than 10 hours or 600 minutes parked in Austin. The amount are not matching this wide amount of time, so to be sure I would remove them.
There are 150446 entries above 600 minutes, and 1 negative that is above 600 minutes. The final table should have 14 894 347 rows */ 

# How many different KioskID we have: 930.
SELECT 
  DISTINCT(KioskID),
  COUNT(*) AS nb
FROM `parking-transactions.main.parking_transactions`
GROUP BY KioskID
ORDER BY KioskID;

# How many different Location Group we have: 27, including the nulls
SELECT 
  DISTINCT(LocationGroup),
  COUNT(*) AS nb
FROM `parking-transactions.main.parking_transactions`
GROUP BY LocationGroup
ORDER BY LocationGroup;
