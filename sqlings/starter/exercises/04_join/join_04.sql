/*

Joins are used a lot in data analysis to explore the nature of the relations in
the data. It is easy to reason about data describing real world things, like
the flight data we use here. We can say with almost 100% certainty, that if a
flight occurs, it will have a destination. Because airplanes can't circle in the
air forever.

However, the data might not always adhere to real world constraints. There is a
possibility that we have flights where the destination is not found from the
airports table. Exploring the nature of these relationsships is a huge part of
working with data, because without being 100% sure how the data is structured,
you cannot be 100% sure that your query will produce the desired output.

Let's look at this exact scenario and TEST if there are indeed destinations
that are not found from the airports table. We have a few possibilities to
achieve this, and you can use whatever strategy you want, but the cleanest is
probably the ANTI JOIN.

Write a query that selects distinct destinations from the flights table that do
not have an entry in the airports table.

*/

select null;
