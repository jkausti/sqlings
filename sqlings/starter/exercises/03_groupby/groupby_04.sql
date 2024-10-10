/*

Another thing that is useful when grouping data, is filtering the result by the
calculated column. Now how could we go about and do that? A simple where clause
one might think! But no, where clauses are always placed before the group by
-statement which leads them to also being evaluated before the grouping occurs.

Fortunately, we have another statement that works for group by clauses, HAVING!

This time, calculate the departure delay (dep_delay column) for each route and
filter the output so that the average departure delay is more than 50. The
output columns should be 'origin', 'destination' and 'avg_dep_delay'.

*/

select null;


