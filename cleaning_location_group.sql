---original parking_transactions_cleaning view modified by adding CASE WHEN for location_group 

SELECT 
   parking_tr.ID AS id
   , parking_tr.Source AS `source`
   , DurationinMinutes AS duration_minute
   , FORMAT_TIMESTAMP('%F %T', StartTime) AS start_time
   , FORMAT_TIMESTAMP('%F %T', EndTime) AS end_time
   , Amount AS amount
   , KioskID AS kiosk_id
   , AppZoneID AS app_zone_id
   , AppZoneGroup AS app_zone_group
   , PaymentMethod AS payment_method
   , CASE
       ---null values replaced with 'Unknown location' 
       WHEN AppZoneID = 101.0 THEN 'Unknown Location'
       ---'Unknown location' replaced with 'South Congress', 'Woods of Westlake', "Dawson's Lot" depending on the AppZoneGroup
       WHEN AppZoneGroup = 'SoCo PTMD'  THEN 'South Congress'
       WHEN AppZoneGroup = 'Woods of Westlake'  THEN 'Woods of Westlake'
       WHEN AppZoneGroup = 'PARD (Parking Lots)' THEN "Dawson's Lot"
       ELSE LocationGroup
     END AS location_group
   , FORMAT_TIMESTAMP('%F %T', LastUpdated) AS last_updated
FROM `parking-transactions.main.parking_transactions` as parking_tr


---Running queries on the updated parking_transactions_cleaning view to double check the results

---Now we have unknown location only if the payment has been done through parking meters source or if the payment was done via app but there is No Zone Group
SELECT DISTINCT `source`, app_zone_group, payment_method, location_group
FROM `parking-transactions.main.parking_transactions_cleaned` 
WHERE location_group = 'Unknown Location'
ORDER BY `source`, app_zone_group, payment_method, location_group;

---No null location_group anymore
SELECT DISTINCT `source`, app_zone_group, payment_method, location_group
FROM `parking-transactions.main.parking_transactions_cleaned` 
WHERE location_group IS NULL
ORDER BY `source`, app_zone_group, payment_method, location_group

--- 110923 passport-web, 6693137 passport-app, 8240734 parking meters
SELECT 
  `source`
  ,COUNT(*) as nb
FROM `parking-transactions.main.parking_transactions_cleaned` 
GROUP BY `source`

---kiosk_id is null when the payment has been done through the app or the web --> 6693137 null values for passport-app and 110923 null values for passport-web
SELECT 
  `source`
  ,COUNT(*) as nb_kiosk_id_null
FROM `parking-transactions.main.parking_transactions_cleaned` 
WHERE kiosk_id IS NULL
GROUP BY `source`

---on the contrary app_zone_id is null when source is parking meters --> 8240734 null values
SELECT 
  `source`
  ,COUNT(*) as nb_appzoneid_null
FROM `parking-transactions.main.parking_transactions_cleaned` 
WHERE app_zone_id IS NULL
GROUP BY `source`


