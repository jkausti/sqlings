
select
    origin,
    destination,
    count(*) as count_route
from data.flights
group by origin, destination;
