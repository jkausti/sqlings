SELECT 
    origin,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN dep_delay > 0 THEN 1 ELSE 0 END) AS delayed_flights,
    AVG(dep_delay) AS avg_all_delay,
    AVG(CASE WHEN dep_delay > 0 THEN dep_delay END) AS avg_delayed_only
FROM 
    data.flights
GROUP BY 
    origin
ORDER BY 
    avg_delayed_only DESC
LIMIT 
    10; 