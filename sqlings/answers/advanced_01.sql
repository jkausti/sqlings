SELECT 
    flight_num, 
    carrier, 
    origin, 
    destination,
    CASE 
        WHEN arr_delay < 0 THEN 'Early'
        WHEN arr_delay = 0 THEN 'On Time'
        WHEN arr_delay BETWEEN 1 AND 15 THEN 'Slight Delay'
        WHEN arr_delay BETWEEN 16 AND 60 THEN 'Moderate Delay'
        WHEN arr_delay > 60 THEN 'Severe Delay'
        ELSE 'Unknown'
    END AS delay_category
FROM 
    data.flights; 