
from data.carriers inner join data.flights
    on carriers.code = flights.carrier
select
    carriers.name,
    flights.origin,
    flights.destination;
