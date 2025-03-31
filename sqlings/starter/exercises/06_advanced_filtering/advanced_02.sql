/*

NULL values require special treatment in SQL. A NULL represents a missing or unknown
value and cannot be compared using standard comparison operators (=, <, >).
Instead, we use IS NULL and IS NOT NULL operators.

In the aircraft table, some aircraft have missing information for their year_built.
Create a query that:

1. Counts the total number of aircraft in the database
2. Counts how many aircraft have a NULL year_built
3. Counts how many aircraft have a non-NULL year_built
4. Shows the average year_built, ignoring NULL values
5. Shows the average year_built, but replaces NULL values with 2000 before calculating

Name the columns as: 'total_aircraft', 'missing_year', 'known_year', 'avg_known_year', 
and 'avg_with_default' respectively.

Hint: Look up the COALESCE function.

*/

select null; 