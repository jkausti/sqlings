/*

Group by clauses are often used for all kinds of aggregations. Let's say we
wanted to calculate the average delay for each route. Then, instead of 'count',
we would use 'avg'! However, mathematical functions require a certain datatype.
Calculating the average of a column of text would surely not yield any
meaningful result!

Write a query that calculates the average arrival delay (arr_delay column) for
each route. The column names in the output should be 'origin', 'destination'
and 'avg_delay'.

*/

select null;
