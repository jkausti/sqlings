/*

Sometimes, we want to keep the non-matched rows for one of the tables that we
are using in the join, even though they do not match any rows in the other
table.
 
This is where the so-called "outer" joins come in handy. In our data we have a
relationship between the 'aiport' table and the 'flights' table. Every flight
has an airport as a destination, while an aiport may be used as destination for
many flights, or non at all!

Write a query that selects the 'destination' column from the flights table and
'full_name' from the airports table. Also make this query only select distinct
values, otherwise we would get a lot of duplicate rows!

We want to display all flights in the output and if the destination has an entry
in the aiports table, it should show the full name.

*/

select null;
