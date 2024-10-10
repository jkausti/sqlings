
select
    *
from data.airports
where (fac_type = 'HELIPORT' or fac_type = 'SEAPLANE BASE') and elevation > 10;

