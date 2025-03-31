/*

The NULLIF function can be useful for handling division by zero errors or for
treating specific values as NULL. NULLIF(expr1, expr2) returns NULL if expr1 equals
expr2; otherwise, it returns expr1.

In the flights table, we want to calculate delay statistics, but some flights have
a delay value of 0, which we want to exclude from some calculations.

Create a query that:

1. Lists the top 10 origin airports with the highest average departure delay
2. For each airport, show:
   - The origin airport code
   - The total number of flights from that airport
   - The number of flights with a departure delay greater than 0
   - The average departure delay (counting all flights)
   - The average departure delay (considering only delayed flights, where delay > 0)

Order the results by the average delay of delayed flights in descending order.

Hint: Use NULLIF to treat 0 delays as NULL for the second average calculation.

*/

select null; 