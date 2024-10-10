
from data.flights left outer join data.airports
on flights.destination = airports.code
select
    distinct
    flights.destination,
    airports.full_name
;
