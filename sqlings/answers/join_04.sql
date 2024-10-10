
from data.flights anti join data.airports
on flights.destination = airports.code
select
    distinct flights.destination;

