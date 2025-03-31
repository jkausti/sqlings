/*

Now let's explore more advanced filtering techniques in SQL, starting with the
powerful CASE expression. CASE allows you to add conditional logic to your
queries, similar to if-else statements in other programming languages.

Using the flights table, create a query that categorizes flights based on their
arrival delay (arr_delay column) with the following categories:
- 'Early': When arr_delay is negative (arrived earlier than scheduled)
- 'On Time': When arr_delay is 0
- 'Slight Delay': When arr_delay is between 1 and 15 minutes
- 'Moderate Delay': When arr_delay is between 16 and 60 minutes
- 'Severe Delay': When arr_delay is more than 60 minutes
- 'Unknown': When arr_delay is NULL

Your query should select the flight_num, carrier, origin, destination, and a new
column called 'delay_category' with the categories above.

*/

select null; 