
select
    origin,
    destination,
    avg(dep_delay) as avg_dep_delay
from data.flights
group by 1, 2
having avg(dep_delay) > 50;
