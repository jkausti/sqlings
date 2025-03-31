SELECT *
FROM data.flights
WHERE (origin = 'JFK' OR origin = 'LAX')
  AND (destination = 'ORD' OR destination = 'DFW')
  AND (flight_time < 180 OR (dep_delay < 15 AND arr_delay < 15))
  AND diverted = 'N'; 