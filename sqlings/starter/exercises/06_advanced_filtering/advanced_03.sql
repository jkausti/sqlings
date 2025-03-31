/*

Complex filtering often requires combining multiple conditions using boolean
operators (AND, OR, NOT). The order of operations and proper use of parentheses
are crucial for getting the expected results.

Create a query that finds all flights meeting ALL of these criteria:
1. Departed from 'JFK' or 'LAX' airports
2. Arrived at 'ORD' or 'DFW' airports
3. Had a flight time less than 180 minutes OR had both departure and arrival delays under 15 minutes
4. Were NOT diverted

Your query should select all columns from the flights table for these flights.

Note: The diverted column contains 'Y' for diverted flights and 'N' for non-diverted flights.

*/

select null; 