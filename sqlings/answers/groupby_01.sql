
select
    origin,
    count(*) as count_origin
from data.flights
group by origin;
