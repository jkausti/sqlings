SELECT 
    f.flight_num,
    f.carrier,
    c.name AS carrier_name,
    f.origin,
    f.destination,
    f.dep_time
FROM 
    data.flights f
JOIN 
    data.carriers c ON f.carrier = c.code
WHERE 
    LOWER(c.name) LIKE '%airlines%'
ORDER BY 
    c.name, 
    f.dep_time; 