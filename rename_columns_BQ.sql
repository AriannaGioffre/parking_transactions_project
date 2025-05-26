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
   , LocationGroup AS location_group
   , FORMAT_TIMESTAMP('%F %T', LastUpdated) AS last_updated
FROM `parking-transactions.main.parking_transactions` as parking_tr
