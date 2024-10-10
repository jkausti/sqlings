/*

Lets look at conditional joins, since those are the ones that are most often
used.

The most common ones are INNER, OUTER and LEFT/RIGHT. Left and right joins are
sometimes called "left outer" and "right outer" and "outer" join is sometimes
called "full outer". The syntax might differ between database implementations so
make sure you read the documentation for the database you are working with when
you use joins! If joins are new to you, I encourage you to read up on the
subject because it might get complicated!

The join condition is similar to the condition that we put in the where clause
and that will determine how the join gets performed and how the rows are
combined.

Lets write a query that uses inner join. Join the carriers table with the
flights that uses the join condition on the 2-letter carrier code that exists in
both tables. Select the 'name' column from the carriers table and the 'origin'
and 'destination' columns from the flights table.

Tip: When dealing with joins, the order of the expressions might not feel very
logical, especially if you are used to working with a Dataframe library. To
mitigate this, DuckDB supports the from-syntax! So you can actually start with
the from-part and then put the select-part after it. So something like "from
my_table select my_column1, my_column2". Neat!

*/

select null;


