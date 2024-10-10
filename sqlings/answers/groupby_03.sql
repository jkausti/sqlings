
select
    origin,
    destination,
    avg(arr_delay) as avg_delay
from data.flights
group by origin, destination;

