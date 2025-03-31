SELECT 
    COUNT(*) AS total_aircraft,
    COUNT(*) - COUNT(year_built) AS missing_year,
    COUNT(year_built) AS known_year,
    AVG(year_built) AS avg_known_year,
    AVG(COALESCE(year_built, 2000)) AS avg_with_default
FROM 
    data.aircraft; 