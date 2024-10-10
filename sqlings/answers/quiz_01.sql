
from data.flights
    inner join data.aircraft
        on flights.tail_num = aircraft.tail_num
    inner join data.aircraft_models
        on aircraft.aircraft_model_code = aircraft_models.aircraft_model_code
    inner join data.carriers
        on flights.carrier = carriers.code
select
    carriers.name,
    aircraft_models.manufacturer,
    aircraft_models.model,
    count(flights.flight_num) as count_flights
where flights.cancelled = 'N'
group by 1, 2, 3;
