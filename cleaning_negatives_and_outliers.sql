-- The first CTE is to swap the start_time and end_time when the duration is negative

WITH transformation AS (
  SELECT  
    parking_tr.ID AS id,  
    parking_tr.Source AS `source`, 
    DurationinMinutes,
    -- Casting the start and end time to Date time for Date_diff later
    CAST(
      CASE 
        WHEN StartTime > EndTime THEN EndTime
        ELSE StartTime
      END AS DATETIME) AS start_time, 
    CAST(
        CASE
          WHEN StartTime > EndTime THEN StartTime
          ELSE EndTime
        END AS DATETIME 
    ) AS end_time,
    Amount AS amount
   , KioskID AS kiosk_id
   , AppZoneID AS app_zone_id
   , AppZoneGroup AS app_zone_group
   , PaymentMethod AS payment_method
   -- Adding the CASE to remove null values from location_group
   , CASE
        WHEN AppZoneID = 101.0 THEN 'Unknown Location'
        WHEN AppZoneGroup = 'SoCo PTMD'  THEN 'South Congress'
        WHEN AppZoneGroup = 'Woods of Westlake'  THEN 'Woods of Westlake'
        WHEN AppZoneGroup = 'PARD (Parking Lots)' THEN "Dawson's Lot"
        ELSE LocationGroup
      END AS location_group
   , FORMAT_TIMESTAMP('%F %T', LastUpdated) AS last_updated
  FROM `parking-transactions.main.parking_transactions` AS parking_tr
)
SELECT
  id,
  source,
  -- Performing date_diff to only have positive values
  DATE_DIFF(end_time, start_time, MINUTE) AS duration_minutes,
  -- formatting the date_time to remove the T in the original values
  FORMAT_DATETIME('%F %T',DATETIME(start_time)) AS start_time,
  FORMAT_DATETIME('%F %T',DATETIME(end_time)) AS end_time,
  amount,
  kiosk_id, 
  app_zone_group, 
  app_zone_id, 
  payment_method, 
  location_group, 
  last_updated
FROM transformation
-- Filtering out the values above 600 minutes
WHERE DATE_DIFF(end_time, start_time, MINUTE) <= 600
ORDER BY transfo.id
